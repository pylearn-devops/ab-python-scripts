import os
import unittest
from unittest.mock import patch, call
from src.lambda_handler import Lambda_handler
from src.constants import SWARM_CHANNEL, ER_BOT_TEST

class TestLambdaHandler(unittest.TestCase):

    @patch('src.lambda_handler.generate_json_from_pagerduty_data')
    @patch.dict(os.environ, {"BOT_ENV": "sandbox"})
    def test_lambda_handler_sandbox(self, mock_generate_json):
        event = {}
        context = {}
        
        Lambda_handler(event, context)
        
        mock_generate_json.assert_called_once_with(channel_id=ER_BOT_TEST)

    @patch('src.lambda_handler.generate_json_from_pagerduty_data')
    @patch.dict(os.environ, {"BOT_ENV": "production"})
    def test_lambda_handler_production(self, mock_generate_json):
        event = {}
        context = {}
        
        Lambda_handler(event, context)
        
        mock_generate_json.assert_called_once_with(channel_id=SWARM_CHANNEL)

    @patch('src.lambda_handler.generate_json_from_pagerduty_data')
    @patch.dict(os.environ, {}, clear=True)
    def test_lambda_handler_no_env(self, mock_generate_json):
        event = {}
        context = {}
        
        Lambda_handler(event, context)
        
        mock_generate_json.assert_called_once_with(channel_id=SWARM_CHANNEL)

if __name__ == '__main__':
    unittest.main()