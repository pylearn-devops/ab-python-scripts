from github import Github
from datetime import datetime, timedelta, timezone
import csv
import os

# GitHub token
GITHUB_TOKEN = 'your_github_token'

# List of organizations
ORGANIZATIONS = ['org1', 'org2', 'org3']

# List of labels to exempt from closing
EXEMPT_LABELS = ['do-not-close', 'important', 'keep-open']

# Repository to push the CSV files
TARGET_REPO = 'your_username/target_repo'
TARGET_FOLDER = 'closed_prs_issues'

# Initialize Github instance
g = Github(GITHUB_TOKEN)

# Define the cutoff date (one year ago from now), with timezone awareness
cutoff_date = datetime.now(timezone.utc) - timedelta(days=365)

# Function to check if an item has any exempt labels
def has_exempt_labels(item):
    for label in item.labels:
        if label.name in EXEMPT_LABELS:
            return True
    return False

# Function to close pull requests and issues with a comment
def close_pulls_and_issues(org_name):
    org = g.get_organization(org_name)
    repos = org.get_repos()
    
    closed_prs = []
    closed_issues = []
    exempt_prs = []
    exempt_issues = []
    closed_count = 0
    max_to_close = 30

    for repo in repos:
        # Close open pull requests older than a year
        pull_requests = repo.get_pulls(state='open')
        for pr in pull_requests:
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if pr.created_at < cutoff_date:
                if has_exempt_labels(pr):
                    exempt_prs.append([pr.number, pr.title, pr.user.login, pr.created_at, repo.name])
                else:
                    pr.create_issue_comment("This pull request has been automatically closed due to inactivity.")
                    pr.edit(state='closed')
                    closed_prs.append([pr.number, pr.title, pr.user.login, pr.created_at, pr.closed_at, repo.name])
                    closed_count += 1
                    print(f"Closed PR: {pr.title} in repo {repo.name}")

        # Close open issues older than a year
        issues = repo.get_issues(state='open')
        for issue in issues:
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if issue.created_at < cutoff_date and issue.pull_request is None:
                if has_exempt_labels(issue):
                    exempt_issues.append([issue.number, issue.title, issue.user.login, issue.created_at, repo.name])
                else:
                    issue.create_comment("This issue has been automatically closed due to inactivity.")
                    issue.edit(state='closed')
                    closed_issues