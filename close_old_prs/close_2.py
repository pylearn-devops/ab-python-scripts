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
                break
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
                break
            if issue.created_at < cutoff_date and issue.pull_request is None:
                if has_exempt_labels(issue):
                    exempt_issues.append([issue.number, issue.title, issue.user.login, issue.created_at, repo.name])
                else:
                    issue.create_comment("This issue has been automatically closed due to inactivity.")
                    issue.edit(state='closed')
                    closed_issues.append([issue.number, issue.title, issue.user.login, issue.created_at, issue.closed_at, repo.name])
                    closed_count += 1
                    print(f"Closed issue: {issue.title} in repo {repo.name}")

    return closed_prs, closed_issues, exempt_prs, exempt_issues

# Function to save data to CSV
def save_to_csv(filename, data, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Function to push CSV to a different repo
def push_csv_to_repo(repo_name, folder, filename):
    repo = g.get_repo(repo_name)
    with open(filename, 'r') as file:
        content = file.read()
    
    path = f"{folder}/{filename}"
    try:
        contents = repo.get_contents(path)
        repo.update_file(contents.path, "Update closed PRs/issues CSV", content, contents.sha)
    except Exception:
        repo.create_file(path, "Add closed PRs/issues CSV", content)

# Main function to close PRs and issues for all organizations
def close_pulls_and_issues_for_orgs():
    all_closed_prs = []
    all_closed_issues = []
    all_exempt_prs = []
    all_exempt_issues = []

    for org in ORGANIZATIONS:
        closed_prs, closed_issues, exempt_prs, exempt_issues = close_pulls_and_issues(org)
        all_closed_prs.extend(closed_prs)
        all_closed_issues.extend(closed_issues)
        all_exempt_prs.extend(exempt_prs)
        all_exempt_issues.extend(exempt_issues)

        if len(all_closed_prs) + len(all_closed_issues) >= 30:
            break

    # Save PRs and issues to CSV files
    if all_closed_prs:
        save_to_csv("closed_prs.csv", all_closed_prs, ["PR Number", "Title", "User", "Created At", "Closed At", "Repository"])
    if all_closed_issues:
        save_to_csv("closed_issues.csv", all_closed_issues, ["Issue Number", "Title", "User", "Created At", "Closed At", "Repository"])

    # Push CSV files to the target repo
    if os.path.exists("closed_prs.csv"):
        push_csv_to_repo(TARGET_REPO, TARGET_FOLDER, "closed_prs.csv")
    if os.path.exists("closed_issues.csv"):
        push_csv_to_repo(TARGET_REPO, TARGET_FOLDER, "closed_issues.csv")

    # Print exempt PRs and issues
    print("\nExempt PRs:")
    for pr in all_exempt_prs:
        print(pr)
    
    print("\nExempt Issues:")
    for issue in all_exempt_issues:
        print(issue)

    print(f"\nTotal closed PRs: {len(all_closed_prs)}")
    print(f"Total closed issues: {len(all_closed_issues)}")

# Execute the main function
if __name__ == "__main__":
    close_pulls_and_issues_for_orgs()