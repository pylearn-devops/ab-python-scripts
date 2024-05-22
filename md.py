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

# Create the Markdown table
markdown_table = "| Policy Name | Policy Link | Policy ID |\n"
markdown_table += "|-------------|-------------|-----------|\n"

for name, link, policy_id in policies:
    markdown_table += f"| {name} | [{link}]({link}) | {policy_id} |\n"

# Print the Markdown table
print(markdown_table)