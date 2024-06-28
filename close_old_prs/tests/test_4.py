import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from src.close_stale_prs_issues import has_exempt_labels, close_pulls_and_issues, close_pulls_and_issues_for_orgs
from src.constants import EXEMPT_LABELS

class TestCloseStalePrsIssues(unittest.TestCase):
    
    def setUp(self):
        # Setup common test data
        self.exempt_labels = EXEMPT_LABELS
        self.mock_label_exempt = MagicMock()
        self.mock_label_exempt.name = self.exempt_labels[0]

        self.mock_label_non_exempt = MagicMock()
        self.mock_label_non_exempt.name = "non-exempt-label"
        
        self.mock_item_with_exempt_label = MagicMock()
        self.mock_item_with_exempt_label.labels = [self.mock_label_exempt]
        
        self.mock_item_without_exempt_label = MagicMock()
        self.mock_item_without_exempt_label.labels = [self.mock_label_non_exempt]

        self.mock_repo = MagicMock()
        self.mock_repo.get_pulls.return_value = [self.mock_item_with_exempt_label, self.mock_item_without_exempt_label]
        self.mock_repo.get_issues.return_value = [self.mock_item_with_exempt_label, self.mock_item_without_exempt_label]

    def test_has_exempt_labels_true(self):
        # Test item with an exempt label
        result = has_exempt_labels(self.mock_item_with_exempt_label)
        self.assertTrue(result)

    def test_has_exempt_labels_false(self):
        # Test item without an exempt label
        result = has_exempt_labels(self.mock_item_without_exempt_label)
        self.assertFalse(result)

    @patch('src.close_stale_prs_issues.get_secret')
    @patch('src.close_stale_prs_issues.Github')
    def test_close_pulls_and_issues(self, mock_github, mock_get_secret):
        # Mocking GitHub token and organization details
        mock_github_instance = mock_github.return_value
        mock_github_instance.get_organization.return_value.get_repos.return_value = [self.mock_repo]
        
        # Mock the get_secret function to return a dictionary with the token
        mock_get_secret.side_effect = lambda key: {"git_api_token": "mock_token"}[key]
        
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues("mock_org")
        
        # Assertions
        self.assertEqual(closed_count, 0)
        self.assertEqual(len(exempt_prs), 1)
        self.assertEqual(len(exempt_issues), 1)
    
    @patch('src.close_stale_prs_issues.close_pulls_and_issues')
    @patch('src.close_stale_prs_issues.get_secret')
    def test_close_pulls_and_issues_for_orgs(self, mock_get_secret, mock_close_pulls_and_issues):
        # Mocking the close_pulls_and_issues function
        mock_close_pulls_and_issues.return_value = (0, [], [])
        
        # Mock the get_secret function to return a dictionary with the token
        mock_get_secret.side_effect = lambda key: {"git_api_token": "mock_token"}[key]

        close_pulls_and_issues_for_orgs()
        
        # Assertions to ensure the mocked function was called
        self.assertTrue(mock_close_pulls_and_issues.called)

if __name__ == '__main__':
    unittest.main()