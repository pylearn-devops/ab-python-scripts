from github import Github
import os
import random
import string

GITHUB_TOKEN = ''

# Initialize Github instance
g = Github(base_url="https://api.github.com", login_or_token=GITHUB_TOKEN)

# Variables
repo_name = "pylearn-devops/test-stale"
branch_prefix = "test-branch-"
num_pulls = 60
file_to_change = "README.md"

# Get the repository
repo = g.get_repo(repo_name)


# Function to create a random string
def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Create pull requests
for i in range(num_pulls):
    branch_name = f"{branch_prefix}{i}"
    # Get the main branch
    main_branch = repo.get_branch("master")

    # Create a new branch from the main branch
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)

    # Get the file contents
    contents = repo.get_contents(file_to_change, ref=branch_name)

    # Create random changes
    new_content = contents.decoded_content.decode("utf-8") + f"\nRandom change {random_string()}"

    # Update the file in the new branch
    repo.update_file(contents.path, f"Random change {i}", new_content, contents.sha, branch=branch_name)

    # Create the pull request
    pr = repo.create_pull(
        title=f"Test Pull Request {i}",
        body="This is a test pull request with random changes.",
        head=branch_name,
        base="master"
    )
    print(f"Created pull request {pr.number}")

print("Done creating pull requests!")
