Sure! You can extend the script to exempt pull requests and issues from closing if they have certain GitHub labels. Below is the updated script with the exemption logic:

```python
from github import Github
from datetime import datetime, timedelta

# GitHub token
GITHUB_TOKEN = 'your_github_token'

# List of organizations
ORGANIZATIONS = ['org1', 'org2', 'org3']

# List of labels to exempt from closing
EXEMPT_LABELS = ['do-not-close', 'important', 'keep-open']

# Initialize Github instance
g = Github(GITHUB_TOKEN)

# Define the cutoff date (one year ago from now)
cutoff_date = datetime.now() - timedelta(days=365)

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
    
    closed_count = 0
    max_to_close = 30

    for repo in repos:
        # Close open pull requests older than a year
        pull_requests = repo.get_pulls(state='open')
        for pr in pull_requests:
            if closed_count >= max_to_close:
                return closed_count
            if pr.created_at < cutoff_date and not has_exempt_labels(pr):
                pr.create_issue_comment("This pull request has been automatically closed due to inactivity.")
                pr.edit(state='closed')
                closed_count += 1
                print(f"Closed PR: {pr.title} in repo {repo.name}")

        # Close open issues older than a year
        issues = repo.get_issues(state='open')
        for issue in issues:
            if closed_count >= max_to_close:
                return closed_count
            if issue.created_at < cutoff_date and issue.pull_request is None and not has_exempt_labels(issue):  # Exclude pull requests
                issue.create_comment("This issue has been automatically closed due to inactivity.")
                issue.edit(state='closed')
                closed_count += 1
                print(f"Closed issue: {issue.title} in repo {repo.name}")

    return closed_count

# Main function to close PRs and issues for all organizations
def close_pulls_and_issues_for_orgs():
    closed_count = 0
    for org in ORGANIZATIONS:
        closed_count += close_pulls_and_issues(org)
        if closed_count >= 30:
            break
    print(f"Total closed PRs and issues: {closed_count}")

# Execute the main function
if __name__ == "__main__":
    close_pulls_and_issues_for_orgs()
```

### Explanation of Changes:

1. **Exempt Labels**: A list of labels (`EXEMPT_LABELS`) that should prevent a pull request or issue from being closed.
2. **Check for Exempt Labels**: The `has_exempt_labels` function checks if an item (pull request or issue) has any of the exempt labels.
3. **Condition for Closing**: The script only closes pull requests and issues if they do not have any of the exempt labels.

### Usage:

1. **Run the Script**: Schedule this script to run once a week.
2. **Token and Organizations**: Ensure your GitHub token and the list of organizations are correctly set.
3. **Labels to Exempt**: Update the `EXEMPT_LABELS` list with the labels you want to use for exemption.

With this script, pull requests and issues with specified labels will be exempt from automatic closing, ensuring that important items remain open.