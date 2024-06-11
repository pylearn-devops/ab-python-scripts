const { Probot } = require("probot");
const moment = require("moment");
const scheduler = require("probot-scheduler");

module.exports = (app) => {
  scheduler(app, { interval: 24 * 60 * 60 * 1000 }); // Runs daily

  app.on("schedule.repository", async (context) => {
    const sixMonthsAgo = moment().subtract(6, 'months').toISOString();
    const owner = context.payload.repository.owner.login;
    const repo = context.payload.repository.name;

    // Function to close old issues
    const closeOldIssues = async () => {
      const issues = await context.octokit.issues.listForRepo({
        owner,
        repo,
        state: "open",
        since: sixMonthsAgo,
      });

      for (const issue of issues.data) {
        if (moment(issue.created_at).isBefore(sixMonthsAgo)) {
          await context.octokit.issues.update({
            owner,
            repo,
            issue_number: issue.number,
            state: "closed",
          });
        }
      }
    };

    // Function to close old pull requests
    const closeOldPRs = async () => {
      const pulls = await context.octokit.pulls.list({
        owner,
        repo,
        state: "open",
        sort: "created",
        direction: "asc",
      });

      for (const pull of pulls.data) {
        if (moment(pull.created_at).isBefore(sixMonthsAgo)) {
          await context.octokit.pulls.update({
            owner,
            repo,
            pull_number: pull.number,
            state: "closed",
          });
        }
      }
    };

    await closeOldIssues();
    await closeOldPRs();
  });

  app.on("issue_comment.created", async (context) => {
    const issue = context.payload.issue;
    const repo = context.payload.repository;
    const comment = context.payload.comment;

    // Check if the issue is closed and the comment is made by a user (not a bot)
    if (issue.state === "closed" && !comment.user.type === "Bot") {
      await context.octokit.issues.update({
        owner: repo.owner.login,
        repo: repo.name,
        issue_number: issue.number,
        state: "open",
      });
    }
  });
};