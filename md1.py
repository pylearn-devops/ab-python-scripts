import pdpyras

# Initialize the PagerDuty API session with your API key
api_key = 'YOUR_PAGERDUTY_API_KEY'
session = pdpyras.APISession(api_key)

# List of escalation policy IDs
escalation_policy_ids = ['P12345', 'P67890', 'P111213']  # Replace with your actual IDs

# Base URL for constructing the HTML links
base_url = "https://yourpagerdutyinstance.pagerduty.com/escalation_policies"

# Function to get escalation policy details
def get_escalation_policy_details(policy_id):
    return session.rget(f'escalation_policies/{policy_id}')

# List to store the policy details
policies = []

# Fetch the policy details for each ID
for policy_id in escalation_policy_ids:
    policy = get_escalation_policy_details(policy_id)
    policy_name = policy['name']
    policy_link = f"{base_url}/{policy_id}"
    policies.append((policy_name, policy_link, policy_id))

# Determine the maximum length for each column
max_name_len = max(len(policy[0]) for policy in policies)
max_link_len = max(len(policy[1]) for policy in policies)
max_id_len = max(len(policy[2]) for policy in policies)

# Create the Markdown table with aligned columns
markdown_table = f"| {'Policy Name'.ljust(max_name_len)} | {'Policy Link'.ljust(max_link_len)} | {'Policy ID'.ljust(max_id_len)} |\n"
markdown_table += f"| {'-' * max_name_len} | {'-' * max_link_len} | {'-' * max_id_len} |\n"

for name, link, policy_id in policies:
    markdown_table += f"| {name.ljust(max_name_len)} | {link.ljust(max_link_len)} | {policy_id.ljust(max_id_len)} |\n"

# Print the Markdown table
print(markdown_table)