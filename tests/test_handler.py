import unittest
from unittest.mock import patch, MagicMock

class TestLambdaHandler(unittest.TestCase):

    @patch('src.opl_swarm.generate_json_from_pagerduty_data')
    @patch('os.getenv')
    def test_lambda_handler_sandbox(self, mock_getenv, mock_generate_json):
        from src.your_module import Lambda_handler

        mock_getenv.return_value = "sandbox"
        mock_event = {}
        mock_context = {}

        Lambda_handler(mock_event, mock_context)

        mock_generate_json.assert_called_once_with(channel_id="CO4LS6J9JKT")

    @patch('src.opl_swarm.generate_json_from_pagerduty_data')
    @patch('os.getenv')
    def test_lambda_handler_production(self, mock_getenv, mock_generate_json):
        from src.your_module import Lambda_handler

        mock_getenv.return_value = "production"
        mock_event = {}
        mock_context = {}

        Lambda_handler(mock_event, mock_context)

        mock_generate_json.assert_called_once_with(channel_id="CO1GFGA4SQ1")

if __name__ == '__main__':
    unittest.main()