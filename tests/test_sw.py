import unittest
from unittest.mock import patch, MagicMock
import json
import os

# Import the module containing the functions to be tested
import your_module

class TestPagerDutyFunctions(unittest.TestCase):
    @patch('your_module.pdpyras.APISession')
    @patch('your_module.logger')
    def test_get_on_calls(self, mock_logger, mock_APISession):
        # Set up mocks
        mock_session = MagicMock()
        mock_APISession.return_value = mock_session
        mock_session.get.return_value = {'escalation_policy': {'name': 'Test Policy'}}
        mock_session.iter_all.return_value = [{'user': {'summary': 'User1'}, 'escalation_level': 1}]

        # Call the function to be tested
        result = your_module.get_on_calls(['test_policy_id'])

        # Assertions
        self.assertEqual(result, {'Test Policy': ['User1']})
        mock_logger.info.assert_called_once_with("Posting Bogie L3 on-call reminder in one-pipeline-swarm slack channel")

    @patch('your_module.get_on_calls')
    @patch('your_module.logger')
    @patch('your_module.slack_post')
    def test_generate_json_from_pagerduty_data(self, mock_slack_post, mock_logger, mock_get_on_calls):
        # Set up mocks
        mock_get_on_calls.return_value = {'Test Policy': ['User1']}
        
        # Call the function to be tested
        your_module.generate_json_from_pagerduty_data()

        # Assertions
        mock_slack_post.assert_called_once()
        mock_logger.debug.assert_called_once()

if __name__ == '__main__':
    unittest.main()