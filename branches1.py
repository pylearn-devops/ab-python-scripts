from github import Github

# Replace with your GitHub token
GITHUB_TOKEN = 'your_github_token'

# List of repository names in the format 'owner/repo'
repo_list = [
    'owner1/repo1',
    'owner2/repo2',
    # Add more repositories as needed
]

# Branch name to delete and recreate
branch_name = 'opl/del'
source_branch = 'master'

def delete_and_recreate_branch(g, repo_name, branch_name, source_branch):
    try:
        repo = g.get_repo(repo_name)

        # Check if the branch exists
        try:
            ref = repo.get_git_ref(f'heads/{branch_name}')
            ref.delete()
            print(f'Branch {branch_name} deleted in {repo_name}.')
        except:
            print(f'Branch {branch_name} does not exist in {repo_name}, skipping deletion.')

        # Get the SHA of the source branch (master)
        try:
            source_ref = repo.get_git_ref(f'heads/{source_branch}')
            source_sha = source_ref.object.sha

            # Create the new branch from master
            repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=source_sha)
            print(f'Branch {branch_name} created from {source_branch} in {repo_name}.')
        except Exception as e:
            print(f'Error fetching source branch {source_branch} in {repo_name}: {e}')

    except Exception as e:
        print(f'Error processing {repo_name}: {e}')

if __name__ == "__main__":
    # Authenticate with GitHub
    g = Github(GITHUB_TOKEN)

    # Process each repository in the list
    for repo_name in repo_list:
        delete_and_recreate_branch(g, repo_name, branch_name, source_branch)