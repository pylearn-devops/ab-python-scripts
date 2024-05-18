import json
from behave import given, when, then
from unittest.mock import patch, Mock
from src.your_module import generate_json_from_pagerduty_data

@given('the following escalation policies')
def step_given_escalation_policies(context):
    context.escalation_policy_ids = [row['policy_id'] for row in context.table]

@given('the following users')
def step_given_users(context):
    context.users = {row['user_id']: {'name': row['name'], 'email': row['email']} for row in context.table}

@when('I generate the JSON from PagerDuty data')
def step_when_generate_json(context):
    # Mocking the necessary functions
    context.mock_get = patch('src.your_module.session.get').start()
    context.mock_iter_all = patch('src.your_module.session.iter_all').start()
    context.mock_sg = patch('src.your_module.sg').start()
    context.mock_get_slack_user_id = patch('src.your_module.get_slack_user_id', return_value='U12345').start()

    # Set up the mock responses
    def mock_get(url):
        if url.startswith('escalation_policies/'):
            return Mock(status_code=200, json=lambda: {'escalation_policy': {'name': 'Policy One'}})
        elif url.startswith('users/'):
            user_id = url.split('/')[-1]
            return Mock(status_code=200, json=lambda: {'user': context.users[user_id]})

    context.mock_get.side_effect = mock_get
    context.mock_iter_all.return_value = [
        {'escalation_level': 1, 'user': {'id': 'U1'}},
        {'escalation_level': 1, 'user': {'id': 'U2'}}
    ]

    # Call the function to generate the JSON
    context.result = generate_json_from_pagerduty_data()

@then('the result should contain the policy and user details')
def step_then_result_should_contain_details(context):
    expected_result = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Hello! Here's today's on-call schedule for your convenience.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Policy One - <@U12345>, <@U12345>"
            }
        }
    ]
    assert context.result == expected_result

@then('the Slack message should be sent with the correct details')
def step_then_slack_message_should_be_sent(context):
    context.mock_sg.assert_called_once_with([
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Hello! Here's today's on-call schedule for your convenience.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Policy One - <@U12345>, <@U12345>"
            }
        }
    ])

    # Stop the mocks after the test
    patch.stopall()