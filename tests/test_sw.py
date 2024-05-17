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
