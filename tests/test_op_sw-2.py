import unittest
from unittest.mock import patch, MagicMock
from your_module import get_on_calls

class TestYourModule(unittest.TestCase):

    def setUp(self):
        self.api_key = "dummy_api_key"
        self.secrets = {"pd_api_token": self.api_key}
        self.policy_data = {
            "id": "P1234",
            "name": "Policy 1",
        }
        self.user_data = {
            "user": {
                "id": "U123",
                "name": "User 1",
                "email": "user1@example.com"
            }
        }

    @patch('your_module.pdpyras.APISession')
    def test_get_on_calls(self, MockAPISession):
        # Mock the session object and its methods
        mock_session = MockAPISession.return_value

        # Mock the response for the escalation policy
        def mock_get(url):
            if "escalation_policies" in url:
                return MagicMock(json=lambda: {"escalation_policy": self.policy_data})
            elif "users" in url:
                return MagicMock(json=lambda: self.user_data)
            return None

        mock_session.get.side_effect = mock_get

        # Mock the iter_all method for on_calls
        mock_session.iter_all.return_value = [
            {"escalation_level": 1, "user": {"id": "U123"}},
            {"escalation_level": 2, "user": {"id": "U456"}}
        ]

        escalation_policy_ids = ["P1234"]
        on_call_emails_by_policy = get_on_calls(escalation_policy_ids)
        
        expected_result = {
            "Policy 1": ["user1@example.com"]
        }

        self.assertEqual(on_call_emails_by_policy, expected_result)

    # Other tests...

if __name__ == '__main__':
    unittest.main()