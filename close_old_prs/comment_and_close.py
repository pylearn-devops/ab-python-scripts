import json
from github import Github
from datetime import datetime, timezone, timedelta

# GitHub token
GITHUB_TOKEN = 'your_github_token'

# List of organizations
ORGANIZATIONS = ['org1', 'org2', 'org3']

# List of labels to exempt from commenting and closing
EXEMPT_LABELS = ['do-not-close', 'important', 'keep-open']

# Initialize Github instance
g = Github(GITHUB_TOKEN)

# Define the ignored date (September 30, 2023)
ignored_date = datetime(2023, 9, 30, tzinfo=timezone.utc)

# Function to check if an item has any exempt labels
def has_exempt_labels(item):
    for label in item.labels:
        if label.name in EXEMPT_LABELS:
            return True
    return False

# Function to comment on pull requests and issues
def comment_on_pulls_and_issues():
    commented_count = 0
    max_to_comment = 30

    for org_name in ORGANIZATIONS:
        org = g.get_organization(org_name)
        repos = org.get_repos()

        for repo in repos:
            # Comment on open pull requests created before the ignored date
            pull_requests = repo.get_pulls(state='open')
            for pr in pull_requests:
                if commented_count >= max_to_comment:
                    break  # Stop processing if we've reached the limit
                if pr.created_at < ignored_date:  # Only consider PRs created before the ignored date
                    if not has_exempt_labels(pr):
                        pr.create_issue_comment(f"@{pr.user.login} This pull request will be automatically closed due to inactivity.")
                        commented_count += 1
                        print(f"Commented on PR: {pr.title} in repo {repo.name}")

            # Comment on open issues created before the ignored date
            issues = repo.get_issues(state='open')
            for issue in issues:
                if commented_count >= max_to_comment:
                    break  # Stop processing if we've reached the limit
                if issue.created_at < ignored_date and issue.pull_request is None:  # Only consider issues created before the ignored date
                    if not has_exempt_labels(issue):
                        issue.create_comment(f"@{issue.user.login} This issue will be automatically closed due to inactivity.")
                        commented_count += 1
                        print(f"Commented on issue: {issue.title} in repo {repo.name}")

# Function to close pull requests and issues
def close_commented_pulls_and_issues():
    closed_count = 0
    max_to_close = 30

    six_days_ago = datetime.now(timezone.utc) - timedelta(days=6)
    comment_identifier = "This pull request will be automatically closed due to inactivity."
    issue_comment_identifier = "This issue will be automatically closed due to inactivity."

    for org_name in ORGANIZATIONS:
        org = g.get_organization(org_name)
        repos = org.get_repos()

        for repo in repos:
            # Close commented pull requests
            pull_requests = repo.get_pulls(state='open')
            for pr in pull_requests:
                if closed_count >= max_to_close:
                    break  # Stop processing if we've reached the limit
                if pr.created_at < ignored_date:  # Only consider PRs created before the ignored date
                    comments = pr.get_issue_comments()
                    for comment in comments:
                        if comment.created_at > six_days_ago and comment.body.startswith(comment_identifier):
                            pr.create_issue_comment("This pull request has been automatically closed due to inactivity.")
                            pr.edit(state='closed')
                            closed_count += 1
                            print(f"Closed PR: {pr.title} in repo {repo.name}")
                            break

            # Close commented issues
            issues = repo.get_issues(state='open')
            for issue in issues:
                if closed_count >= max_to_close:
                    break  # Stop processing if we've reached the limit
                if issue.created_at < ignored_date and issue.pull_request is None:  # Only consider issues created before the ignored date
                    comments = issue.get_comments()
                    for comment in comments:
                        if comment.created_at > six_days_ago and comment.body.startswith(issue_comment_identifier):
                            issue.create_comment("This issue has been automatically closed due to inactivity.")
                            issue.edit(state='closed')
                            closed_count += 1
                            print(f"Closed issue: {issue.title} in repo {repo.name}")
                            break

# Lambda handler
def lambda_handler(event, context):
    action = event.get('action')
    if action == 'comment':
        comment_on_pulls_and_issues()
    elif action == 'close':
        close_commented_pulls_and_issues()
    else:
        raise ValueError("Invalid action specified in event")

# Example event for commenting
event_comment = {
    'action': 'comment'
}

# Example event for closing
event_close = {
    'action': 'close'
}

# Testing the lambda_handler function
if __name__ == "__main__":
    lambda_handler(event_comment, None)  # Uncomment to test commenting
    lambda_handler(event_close, None)  # Uncomment to test closing
