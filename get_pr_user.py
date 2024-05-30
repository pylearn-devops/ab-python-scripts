from github import Github
import pandas as pd

# Replace with your GitHub token
access_token = 'your_access_token'
user_name = 'target_user_name'
org_name = 'organization_name'
csv_filename = 'pull_requests.csv'

# Authenticate to GitHub
g = Github(access_token)

# Get the organization
org = g.get_organization(org_name)

# Initialize an empty list to collect pull request data
pull_requests_data = []

# Iterate through repositories in the organization
for repo in org.get_repos():
    # Get pull requests for the repository
    pulls = repo.get_pulls(state='all')
    for pull in pulls:
        # Check if the pull request was created by the target user
        if pull.user.login == user_name:
            pull_requests_data.append({
                'Repository': repo.name,
                'Pull Request Number': pull.number,
                'Pull Request Title': pull.title
            })

# Convert the list to a pandas DataFrame
df = pd.DataFrame(pull_requests_data)

# Write the DataFrame to a CSV file
df.to_csv(csv_filename, index=False)

print(f"Pull requests have been written to {csv_filename}")