from github import Github
import json

# Personal access token
token = 'your_personal_access_token_here'
g = Github(token)

# The organization to check
org_name = 'current_org_name'

# Load previously stored organization info (if exists)
try:
    with open('org_info.json', 'r') as f:
        prev_org_info = json.load(f)
except FileNotFoundError:
    prev_org_info = {}

# Fetch current organization info
org = g.get_organization(org_name)
current_org_info = {
    'login': org.login,
    'id': org.id,
    'name': org.name,
    'description': org.description,
    'created_at': org.created_at.isoformat(),
    'updated_at': org.updated_at.isoformat(),
}

# Compare with previous information to detect renaming
if 'login' in prev_org_info and prev_org_info['login'] != current_org_info['login']:
    print(f"Organization was renamed from {prev_org_info['login']} to {current_org_info['login']}.")

# Save current organization info for future comparison
with open('org_info.json', 'w') as f:
    json.dump(current_org_info, f)

# Output the current organization info
print(f"Current organization info: {current_org_info}")