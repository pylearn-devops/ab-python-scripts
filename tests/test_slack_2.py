import unittest
from unittest.mock import patch, MagicMock
from slack_sdk.errors import SlackApiError
from src.your_module import slack_post, get_slack_user_id  # Update with the correct module path

class TestSlackFunctions(unittest.TestCase):

    @patch('src.your_module.get_secret')
    @patch('src.your_module.client.chat_postMessage')
    def test_slack_post_success(self, mock_chat_postMessage, mock_get_secret):
        # Arrange
        mock_get_secret.return_value = 'fake_token'
        mock_response = MagicMock()
        mock_response.data = {"ok": True}
        mock_chat_postMessage.return_value = mock_response
        data = {"key": "value"}
        channel_id = "C1234567890"
        
        # Act
        response = slack_post(data, channel_id)
        
        # Assert
        mock_chat_postMessage.assert_called_once_with(
            channel=channel_id,
            text="Hello! Here's today's on-call schedule :smiley:",
            blocks=data
        )
        self.assertEqual(response, mock_response)

    @patch('src.your_module.get_secret')
    @patch('src.your_module.client.chat_postMessage')
    def test_slack_post_failure(self, mock_chat_postMessage, mock_get_secret):
        # Arrange
        mock_get_secret.return_value = 'fake_token'
        mock_chat_postMessage.side_effect = SlackApiError(message="error", response={"error": "some_error"})
        data = {"key": "value"}
        channel_id = "C1234567890"
        
        # Act & Assert
        with self.assertRaises(SlackApiError):
            slack_post(data, channel_id)

    @patch('src.your_module.get_secret')
    @patch('src.your_module.client.users_lookupByEmail')
    def test_get_slack_user_id_success(self, mock_users_lookupByEmail, mock_get_secret):
        # Arrange
        mock_get_secret.return_value = 'fake_token'
        mock_response = {"user": {"id": "U1234567890"}}
        mock_users_lookupByEmail.return_value = mock_response
        email = "oncall@example.com"
        
        # Act
        user_id = get_slack_user_id(email)
        
        # Assert
        mock_users_lookupByEmail.assert_called_once_with(email=email)
        self.assertEqual(user_id, "U1234567890")

    @patch('src.your_module.get_secret')
    @patch('src.your_module.client.users_lookupByEmail')
    def test_get_slack_user_id_failure(self, mock_users_lookupByEmail, mock_get_secret):
        # Arrange
        mock_get_secret.return_value = 'fake_token'
        mock_users_lookupByEmail.side_effect = SlackApiError(message="error", response={"error": "some_error"})
        email = "oncall@example.com"
        
        # Act & Assert
        with self.assertRaises(SlackApiError):
            get_slack_user_id(email)

if __name__ == '__main__':
    unittest.main()