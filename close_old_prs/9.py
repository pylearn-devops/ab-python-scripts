from github import Github
from datetime import datetime, timezone

# GitHub token
GITHUB_TOKEN = 'your_github_token'

# List of organizations
ORGANIZATIONS = ['org1', 'org2', 'org3']

# List of labels to exempt from closing
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

# Function to close pull requests and issues with a comment
def close_pulls_and_issues(org_name):
    org = g.get_organization(org_name)
    repos = org.get_repos()
    
    closed_count = 0
    max_to_close = 30

    exempt_prs = []
    exempt_issues = []

    for repo in repos:
        # Close open pull requests created before the ignored date
        pull_requests = repo.get_pulls(state='open')
        for pr in pull_requests:
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if pr.created_at < ignored_date:  # Only consider PRs created before the ignored date
                if has_exempt_labels(pr):
                    exempt_prs.append([pr.number, pr.title, pr.user.login, pr.created_at, repo.name])
                else:
                    pr.create_issue_comment("This pull request has been automatically closed due to inactivity.")
                    pr.edit(state='closed')
                    closed_count += 1
                    print(f"Closed PR: {pr.title} in repo {repo.name}")

        # Close open issues created before the ignored date
        issues = repo.get_issues(state='open')
        for issue in issues:
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if issue.created_at < ignored_date and issue.pull_request is None:  # Only consider issues created before the ignored date
                if has_exempt_labels(issue):
                    exempt_issues.append([issue.number, issue.title, issue.user.login, issue.created_at, repo.name])
                else:
                    issue.create_comment("This issue has been automatically closed due to inactivity.")
                    issue.edit(state='closed')
                    closed_count += 1
                    print(f"Closed issue: {issue.title} in repo {repo.name}")

    return closed_count, exempt_prs, exempt_issues

# Main function to close PRs and issues for all organizations
def close_pulls_and_issues_for_orgs():
    total_closed_count = 0
    max_to_close = 30

    all_exempt_prs = []
    all_exempt_issues = []

    for org in ORGANIZATIONS:
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues(org)
        total_closed_count += closed_count
        all_exempt_prs.extend(exempt_prs)
        all_exempt_issues.extend(exempt_issues)

        if total_closed_count >= max_to_close:
            break  # Stop processing if we've closed 30 items

    # Print exempt PRs and issues
    print("\nExempt PRs:")
    for pr in all_exempt_prs:
        print(f"PR #{pr[0]}: {pr[1]} by {pr[2]} created on {pr[3]} in repo {pr[4]}")
    
    print("\nExempt Issues:")
    for issue in all_exempt_issues:
        print(f"Issue #{issue[0]}: {issue[1]} by {issue[2]} created on {issue[3]} in repo {issue[4]}")

    print(f"\nTotal exempt PRs: {len(all_exempt_prs)}")
    print(f"Total exempt issues: {len(all_exempt_issues)}")

# Execute the main function
if __name__ == "__main__":
    close_pulls_and_issues_for_orgs()