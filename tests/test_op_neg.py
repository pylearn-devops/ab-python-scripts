import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import pdpyras
from opl_swarm import load_data_from_json, get_on_calls, generate_json_from_pagerduty_data

# Mock data for testing
mock_secrets = {
    'pd_api_token': 'mock_pd_api_token',
    'sandbox_bot_token': 'mock_sandbox_bot_token'
}

mock_json_data = {
    "policy1": ["user1@example.com", "user2@example.com"],
    "policy2": ["user3@example.com"]
}

mock_escalation_policies = {
    "escalation_policies": [
        {"id": "policy1", "name": "Policy 1"},
        {"id": "policy2", "name": "Policy 2"}
    ]
}

mock_on_calls = [
    {"escalation_level": 1, "user": {"id": "user1", "name": "User One", "email": "user1@example.com"}},
    {"escalation_level": 2, "user": {"id": "user2", "name": "User Two", "email": "user2@example.com"}},
]

mock_users_info = [
    {"id": "user1", "name": "User One", "email": "user1@example.com"},
    {"id": "user2", "name": "User Two", "email": "user2@example.com"}
]

class TestOpsSwarm(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps(mock_json_data))
    def test_load_data_from_json(self, mock_open):
        # Test with valid data
        data = load_data_from_json('dummy_path')
        self.assertEqual(data, mock_json_data)
        mock_open.assert_called_once_with('dummy_path', 'r')

        # Test with invalid file path
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_data_from_json('invalid_path')

        # Test with invalid JSON
        mock_open.side_effect = None
        mock_open.return_value.read.return_value = "{invalid_json"
        with self.assertRaises(json.JSONDecodeError):
            load_data_from_json('dummy_path')

    @patch('pdpyras.APISession.get')
    def test_get_on_calls(self, mock_get):
        # Setup mock responses
        mock_get.side_effect = [
            MagicMock(json=lambda: {"escalation_policy": {"name": "Policy 1"}}),
            MagicMock(iter_all=lambda url, params: iter(mock_on_calls)),
            MagicMock(json=lambda: {"user": mock_users_info[0]})
        ]

        session = pdpyras.APISession('mock_api_key')
        
        # Test with valid data
        result = get_on_calls(session, ['policy1'])
        expected_result = {
            "Policy 1": ["user1@example.com"]
        }
        self.assertEqual(result, expected_result)

        # Test with invalid policy ID
        mock_get.side_effect = [
            MagicMock(json=lambda: None),
            MagicMock(iter_all=lambda url, params: iter([]))
        ]
        result = get_on_calls(session, ['invalid_policy'])
        self.assertEqual(result, {})

        # Test with API errors
        mock_get.side_effect = pdpyras.errors.PDClientError("API error")
        with self.assertRaises(pdpyras.errors.PDClientError):
            get_on_calls(session, ['policy1'])

    @patch('opl_swarm.get_on_calls', return_value=mock_json_data)
    @patch('opl_swarm.slack_post')
    @patch('opl_swarm.get_slack_user_id', side_effect=lambda email: f'@{email.split("@")[0]}')
    def test_generate_json_from_pagerduty_data(self, mock_get_on_calls, mock_slack_post, mock_get_slack_user_id):
        channel_id = 'mock_channel_id'

        # Test with valid data
        result = generate_json_from_pagerduty_data(channel_id)
        expected_result = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello! Here's today's on-call schedule for your convenience."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "policy1 - @user1 @user2"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "policy2 - @user3"
                }
            }
        ]
        self.assertEqual(result, expected_result)
        mock_get_on_calls.assert_called_once()
        mock_slack_post.assert_called_once_with(expected_result, channel_id)

        # Test with missing policy names in mapping
        mock_get_on_calls.return_value = {"missing_policy": ["user4@example.com"]}
        result = generate_json_from_pagerduty_data(channel_id)
        expected_result_missing_policy = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello! Here's today's on-call schedule for your convenience."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "missing_policy - @user4"
                }
            }
        ]
        self.assertEqual(result, expected_result_missing_policy)

        # Test with API errors
        mock_get_on_calls.side_effect = pdpyras.errors.PDClientError("API error")
        with self.assertRaises(pdpyras.errors.PDClientError):
            generate_json_from_pagerduty_data(channel_id)

if __name__ == '__main__':
    unittest.main()