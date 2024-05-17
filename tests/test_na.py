import pytest
from unittest.mock import patch, Mock

@patch('src.your_module.get_slack_user_id', return_value='U12345')
@patch('src.your_module.sg')
@patch('src.your_module.session.get')
@patch('src.your_module.session.iter_all')
def test_generate_json_from_pagerduty_data(mock_iter_all, mock_get, mock_sg, mock_get_slack_user_id):
    from src.your_module import generate_json_from_pagerduty_data

    # Mock response for escalation policy
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: {
            'escalation_policy': {'name': 'Policy One'}
        }),
        Mock(status_code=200, json=lambda: {
            'user': {'name': 'User One', 'email': 'user1@example.com'}
        }),
        Mock(status_code=200, json=lambda: {
            'user': {'name': 'User Two', 'email': 'user2@example.com'}
        })
    ]

    # Mock response for iter_all
    mock_iter_all.return_value = [
        {'escalation_level': 1, 'user': {'id': 'U1'}},
        {'escalation_level': 1, 'user': {'id': 'U2'}}
    ]

    # Call the function to test
    generate_json_from_pagerduty_data()

    # Assert that sg (Slack message sending function) is called with the correct arguments
    expected_arguments = [
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
    mock_sg.assert_called_once_with(expected_arguments)

    # Assert that get_slack_user_id is called with the correct email addresses
    mock_get_slack_user_id.assert_called_with('user1@example.com')
    mock_get_slack_user_id.assert_called_with('user2@example.com')

if __name__ == '__main__':
    pytest.main()