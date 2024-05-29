import unittest
from unittest.mock import patch, MagicMock
from your_module import load_data_from_json, get_on_calls, generate_json_from_pagerduty_data

class TestYourModule(unittest.TestCase):
    
    def setUp(self):
        # Set up any initial data or state here
        self.api_key = "dummy_api_key"
        self.secrets = {"pd_api_token": self.api_key}
        self.policy_data = {
            "escalation_policies": [
                {
                    "id": "P1234",
                    "name": "Policy 1",
                },
                {
                    "id": "P5678",
                    "name": "Policy 2",
                }
            ]
        }
        self.user_data = {
            "users": [
                {
                    "id": "U123",
                    "name": "User 1",
                    "email": "user1@example.com"
                },
                {
                    "id": "U456",
                    "name": "User 2",
                    "email": "user2@example.com"
                }
            ]
        }

    @patch('your_module.pdpyras.APISession')
    def test_get_on_calls(self, MockAPISession):
        # Mock the session object and its methods
        mock_session = MockAPISession.return_value
        mock_session.get.return_value.json.return_value = self.policy_data['escalation_policies'][0]
        mock_session.iter_all.return_value = [
            {"escalation_level": 1, "user": {"id": "U123"}},
            {"escalation_level": 2, "user": {"id": "U456"}}
        ]
        mock_session.get.return_value.json.return_value = self.user_data['users'][0]

        escalation_policy_ids = ["P1234", "P5678"]
        on_call_emails_by_policy = get_on_calls(escalation_policy_ids)
        
        expected_result = {
            "Policy 1": ["user1@example.com"],
            "Policy 2": []
        }
        
        self.assertEqual(on_call_emails_by_policy, expected_result)
    
    @patch('your_module.load_data_from_json')
    def test_load_data_from_json(self, mock_load_data):
        mock_load_data.return_value = self.policy_data
        result = load_data_from_json('dummy_path')
        self.assertEqual(result, self.policy_data)
    
    @patch('your_module.get_on_calls')
    @patch('your_module.slack_post')
    def test_generate_json_from_pagerduty_data(self, mock_slack_post, mock_get_on_calls):
        mock_get_on_calls.return_value = {
            "Policy 1": ["user1@example.com", "user2@example.com"],
            "Policy 2": ["user3@example.com"]
        }
        
        channel_id = "C12345"
        result = generate_json_from_pagerduty_data(channel_id)
        
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
                    "text": "Policy 1 - <@user1@example.com>,<@user2@example.com>"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Policy 2 - <@user3@example.com>"
                }
            }
        ]
        
        self.assertEqual(result, expected_result)
        mock_slack_post.assert_called_with(expected_result, channel_id)
    
    def tearDown(self):
        # Clean up any state or data here
        pass

if __name__ == '__main__':
    unittest.main()