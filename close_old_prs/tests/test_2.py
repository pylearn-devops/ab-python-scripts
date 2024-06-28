import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Mocking the imports from src.constants and src.secrets
mock_constants = {
    'GITHUB_URL': 'https://api.github.com',
    'GITHUB_ORGANIZATIONS': ['org1', 'org2'],
    'EXEMPT_LABELS': ['exempt1', 'exempt2'],
    'CLOSE_COMMENT': 'This issue is being closed due to inactivity.',
    'SECRET_KEYS': ['git_api_token']
}

def mock_get_secret(key):
    return 'fake_token' if key == 'git_api_token' else None

class TestHasExemptLabels(unittest.TestCase):
    @patch('src.constants', mock_constants)
    @patch('src.secrets.get_secret', side_effect=mock_get_secret)
    def setUp(self, mock_get_secret, mock_constants):
        # Re-import the module to apply the mocks
        global close_stale_prs_issues
        import close_stale_prs_issues

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
    @patch('src.constants', mock_constants)
    @patch('src.secrets.get_secret', side_effect=mock_get_secret)
    @patch('close_stale_prs_issues.Github')
    def test_initialization(self, mock_github, mock_get_secret, mock_constants):
        # Check if the Github object is initialized with the correct URL and token
        global close_stale_prs_issues
        import close_stale_prs_issues
        
        mock_github.assert_called_with(base_url='https://api.github.com', login_or_token='fake_token')

    @patch('src.constants', mock_constants)
    @patch('src.secrets.get_secret', side_effect=mock_get_secret)
    def test_ignored_date(self, mock_get_secret, mock_constants):
        # Check if the ignored_date is set correctly
        global close_stale_prs_issues
        import close_stale_prs_issues
        
        expected_date = datetime(year=2024, month=6, day=27, tzinfo=timezone.utc)
        self.assertEqual(close_stale_prs_issues.ignored_date, expected_date)

if __name__ == '__main__':
    unittest.main()