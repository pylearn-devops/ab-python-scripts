from github import Github
import random
import string

# Authenticate to GitHub
g = Github("your_access_token")

# Variables
repo_name = "your_username/your_repository"
num_issues = 60

# Get the repository
repo = g.get_repo(repo_name)

# Function to create a random string
def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Create issues
for i in range(num_issues):
    title = f"Random Issue {i+1}: {random_string(5)}"
    body = f"This is a randomly generated issue with random content: {random_string(50)}"
    issue = repo.create_issue(title=title, body=body)
    print(f"Created issue {issue.number}")

print("Done creating issues!")