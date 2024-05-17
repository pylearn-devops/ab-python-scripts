import unittest
from unittest.mock import patch, Mock
import json

class TestPagerDutyModule(unittest.TestCase):

    @patch('pdpyras.APISession')
    @patch('builtins.open', unittest.mock.mock_open(read_data='{"policy1": "Policy One"}'))
    @patch('os.getenv', return_value='dummy_api_key')
    def test_load_data_from_json(self, mock_getenv, mock_open, MockAPISession):
        from your_module import load_data_from_json
        data = load_data_from_json('dummy.json')
        self.assertEqual(data, {"policy1": "Policy One"})
    
  

    @patch('pdpyras.APISession')
    @patch('your_module.session.get')
    @patch('your_module.session.iter_all')
    def test_get_on_calls(self, mock_iter_all, mock_get, MockAPISession):
        from your_module import get_on_calls

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

        escalation_policy_ids = ['P1']
        expected_result = {
            'Policy One': ['user1@example.com', 'user2@example.com']
        }

        result = get_on_calls(escalation_policy_ids)

        self.assertEqual(result, expected_result)
        mock_get.assert_any_call('escalation_policies/P1')
        mock_get.assert_any_call('users/U1')
        mock_get.assert_any_call('users/U2')
        mock_iter_all.assert_called_once_with('oncalls', params={'escalation_policy_ids[]': 'P1'})

    
    @patch('pdpyras.APISession')
    @patch('your_module.get_on_calls')
    @patch('your_module.get_slack_user_id', return_value='U12345')
    @patch('your_module.sg')
    @patch('builtins.open', unittest.mock.mock_open(read_data='{"policy1": "Policy One"}'))
    def test_generate_json_from_pagerduty_data(self, mock_open, mock_sg, mock_get_slack_user_id, mock_get_on_calls, MockAPISession):
        from your_module import generate_json_from_pagerduty_data
        mock_get_on_calls.return_value = {
            "policy1": ["user1@example.com", "user2@example.com"]
        }
        result = generate_json_from_pagerduty_data()
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
        self.assertEqual(result, expected_result)
        mock_sg.assert_called_once_with(expected_result)

if __name__ == '__main__':
    unittest.main()
