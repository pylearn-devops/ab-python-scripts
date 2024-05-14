import os
import unittest
from unittest.mock import MagicMock, patch

from your_module_name import slack_post, get_slack_user_id

class TestSlackFunctions(unittest.TestCase):

    @patch("your_module_name.WebClient.chat_postMessage")
    def test_slack_post(self, mock_chat_post_message):
        mock_response = MagicMock()
        mock_chat_post_message.return_value = mock_response

        data = [{"type": "section", "text": {"type": "mrkdwn", "text": "Hello"}}]
        channel_id = "your_channel_id"

        response = slack_post(data, channel_id)

        mock_chat_post_message.assert_called_once_with(
            channel=channel_id,
            text="Something is wrong with the bot :sweat_smile",
            blocks=data
        )
        self.assertEqual(response, mock_response)

    @patch("your_module_name.WebClient.users_lookupByEmail")
    def test_get_slack_user_id(self, mock_users_lookup_by_email):
        mock_response = {"user": {"id": "your_slack_user_id"}}
        mock_users_lookup_by_email.return_value = mock_response

        oncall_email = "example@example.com"

        slack_user_id = get_slack_user_id(oncall_email)

        mock_users_lookup_by_email.assert_called_once_with(email=oncall_email)
        self.assertEqual(slack_user_id, mock_response["user"]["id"])

if __name__ == "__main__":
    unittest.main()