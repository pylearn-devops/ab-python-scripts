import { Octokit } from '@octokit/rest';
import { App } from '@octokit/app';
import { createAppAuth } from '@octokit/auth-app';
import schedule from 'node-schedule';
import yaml from 'yaml';
import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

const { GITHUB_APP_ID } = process.env;

// Read private key from file synchronously
const privateKeyPath = 'private-key.pem'; // Replace with your actual path
const privateKey = fs.readFileSync(privateKeyPath, 'utf8');

// Create an App instance
const app = new App({
    appId: GITHUB_APP_ID,
    privateKey: privateKey,
});

// Function to get an authenticated Octokit instance for a specific installation
const getInstallationOctokit = async (installationId) => {
    const auth = createAppAuth({
        appId: process.env.GITHUB_APP_ID,
        privateKey: privateKey,
        installationId,
    });

    const { token } = await auth({ type: 'installation' });

    return new Octokit({
        auth: token,
    });
};

// Function to fetch configuration from the repository
const getConfig = async (octokit, owner, repo) => {
    try {
        const { data } = await octokit.repos.getContent({
            owner,
            repo,
            path: '.github/close-config.yml',
        });

        const content = Buffer.from(data.content, 'base64').toString('utf-8');
        return yaml.parse(content);
    } catch (error) {
        if (error.status === 404) {
            console.error('Config file not found:', error.message);
            return {
                closeAfterDays: 30,
                exemptLabels: [],
                closeComment: 'This item has been automatically closed due to inactivity.',
            };
        }
        console.error('Error fetching config:', error);
        throw error; // re-throw the error for further handling
    }
};


// Function to close stale issues and pull requests
const closeStaleItems = async (octokit, owner, repo) => {
    const config = await getConfig(octokit, owner, repo);
    const closeAfterDays = config.closeAfterDays || 30;
    const exemptLabels = config.exemptLabels || [];
    const closeComment = config.closeComment || 'This item has been automatically closed due to inactivity.';
    const closeDate = new Date(Date.now() - closeAfterDays * 24 * 60 * 60 * 1000);

    const isExempt = (labels) => {
        return labels.some(label => exemptLabels.includes(label.name));
    };

    const closeStaleIssues = async () => {
        const issues = await octokit.paginate(octokit.rest.issues.listForRepo, {
            owner,
            repo,
            state: 'open',
        });

        for (const issue of issues) {
            const updatedAt = new Date(issue.updated_at);
            if (updatedAt < closeDate && !isExempt(issue.labels)) {
                await octokit.rest.issues.update({
                    owner,
                    repo,
                    issue_number: issue.number,
                    state: 'closed',
                });
                await octokit.rest.issues.createComment({
                    owner,
                    repo,
                    issue_number: issue.number,
                    body: closeComment,
                });
                console.log(`Closed issue #${issue.number} in ${owner}/${repo} in organization ${owner}`);
            }
        }
    };

    const closeStalePullRequests = async () => {
        const pulls = await octokit.paginate(octokit.rest.pulls.list, {
            owner,
            repo,
            state: 'open',
        });

        for (const pull of pulls) {
            const updatedAt = new Date(pull.updated_at);
            if (updatedAt < closeDate && !isExempt(pull.labels)) {
                await octokit.rest.pulls.update({
                    owner,
                    repo,
                    pull_number: pull.number,
                    state: 'closed',
                });
                await octokit.rest.issues.createComment({
                    owner,
                    repo,
                    issue_number: pull.number,
                    body: closeComment,
                });
                console.log(`Closed pull request #${pull.number} in ${owner}/${repo} in organization ${owner}`);
            }
        }
    };

    await closeStaleIssues();
    await closeStalePullRequests();
};

// Express server to handle webhooks
const server = express();
server.use(bodyParser.json());

const handleWebhookEvent = async (event) => {
    try {
        // Ensure event and necessary properties are present
        if (!event || !event.repository || !event.repository.id) {
            console.error('Invalid or incomplete webhook event:', event);
            return;
        }

        const { action, repository } = event;
        const owner = repository.owner.login;
        const repo = repository.name;

        console.log(`Received action: ${action}`);

        // Handle the webhook event according to your needs
        console.log(event);
    } catch (error) {
        console.error('Error handling webhook event:', error);
    }
};

server.post('/webhook', async (req, res) => {
    const event = req.body;
    try {
        await handleWebhookEvent(event);
        res.status(200).send('OK');
    } catch (error) {
        console.error('Error handling webhook event:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Schedule the job to run every 5 minutes for testing purposes
schedule.scheduleJob('*/1 * * * *', async () => {
    const appOctokit = new Octokit({
        authStrategy: createAppAuth,
        auth: {
            appId: process.env.GITHUB_APP_ID,
            privateKey: privateKey,
        },
    });

    const installations = await appOctokit.paginate('GET /app/installations');

    for (const installation of installations) {
        const installationId = installation.id;
        const octokit = await getInstallationOctokit(installationId);

        const repos = await octokit.paginate(octokit.apps.listReposAccessibleToInstallation, {
            installation_id: installationId,
        });

        for (const repo of repos) {
            await closeStaleItems(octokit, repo.owner.login, repo.name);
        }
    }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
