import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Mocking the imports from src.constants and src.secrets
with patch('src.constants') as mock_constants, patch('src.secrets.get_secret') as mock_get_secret:
    # Define mock constants
    mock_constants.GITHUB_URL = 'https://api.github.com'
    mock_constants.GITHUB_ORGANIZATIONS = ['org1', 'org2']
    mock_constants.EXEMPT_LABELS = ['exempt1', 'exempt2']
    mock_constants.CLOSE_COMMENT = 'This issue is being closed due to inactivity.'
    mock_constants.SECRET_KEYS = ['git_api_token']
    
    # Mock get_secret function
    mock_get_secret.return_value = 'fake_token'

    # Import the code to be tested
    import close_stale_prs_issues

    class TestHasExemptLabels(unittest.TestCase):
        def test_has_exempt_labels_with_exempt_label(self):
            item = MagicMock()
            item.labels = [MagicMock(name='exempt1')]

            self.assertTrue(close_stale_prs_issues.has_exempt_labels(item))

        def test_has_exempt_labels_without_exempt_label(self):
            item = MagicMock()
            item.labels = [MagicMock(name='not_exempt')]

            self.assertFalse(close_stale_prs_issues.has_exempt_labels(item))

        def test_has_exempt_labels_with_multiple_labels(self):
            item = MagicMock()
            item.labels = [MagicMock(name='not_exempt'), MagicMock(name='exempt2')]

            self.assertTrue(close_stale_prs_issues.has_exempt_labels(item))

        def test_has_exempt_labels_with_empty_labels(self):
            item = MagicMock()
            item.labels = []

            self.assertFalse(close_stale_prs_issues.has_exempt_labels(item))

    class TestInitialization(unittest.TestCase):
        @patch('close_stale_prs_issues.Github')
        def test_initialization(self, mock_github):
            # Check if the Github object is initialized with the correct URL and token
            mock_github.assert_called_with(base_url='https://api.github.com', login_or_token='fake_token')

        def test_ignored_date(self):
            # Check if the ignored_date is set correctly
            expected_date = datetime(year=2024, month=6, day=27, tzinfo=timezone.utc)
            self.assertEqual(close_stale_prs_issues.ignored_date, expected_date)

    if __name__ == '__main__':
        unittest.main()