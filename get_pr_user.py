from github import Github
import csv

# Replace with your GitHub token
access_token = 'your_access_token'
user_name = 'target_user_name'
org_name = 'organization_name'
csv_filename = 'pull_requests.csv'

# Authenticate to GitHub
g = Github(access_token)

# Get the organization
org = g.get_organization(org_name)

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Repository', 'Pull Request Number', 'Pull Request Title'])

    # Iterate through repositories in the organization
    for repo in org.get_repos():
        # Get pull requests for the repository
        pulls = repo.get_pulls(state='all')
        for pull in pulls:
            # Check if the pull request was created by the target user
            if pull.user.login == user_name:
                writer.writerow([repo.name, pull.number, pull.title])

print(f"Pull requests have been written to {csv_filename}")