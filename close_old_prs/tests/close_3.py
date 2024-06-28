import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from src.close_stale_prs_issues import has_exempt_labels, close_pulls_and_issues, close_pulls_and_issues_for_orgs

class TestCloseStalePrsIssues(unittest.TestCase):
    
    def setUp(self):
        # Setup common test data
        self.exempt_labels = ["do-not-close", "important"]
        self.mock_item_with_exempt_label = MagicMock()
        self.mock_item_with_exempt_label.labels = [MagicMock(name="do-not-close")]
        
        self.mock_item_without_exempt_label = MagicMock()
        self.mock_item_without_exempt_label.labels = [MagicMock(name="bug")]

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
        mock_github.return_value.get_organization.return_value.get_repos.return_value = [self.mock_repo]
        mock_get_secret.return_value = "mock_token"
        
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues("mock_org")
        
        # Assertions
        self.assertEqual(closed_count, 0)
        self.assertEqual(len(exempt_prs), 1)
        self.assertEqual(len(exempt_issues), 1)
    
    @patch('src.close_stale_prs_issues.close_pulls_and_issues')
    def test_close_pulls_and_issues_for_orgs(self, mock_close_pulls_and_issues):
        # Mocking the close_pulls_and_issues function
        mock_close_pulls_and_issues.return_value = (0, [], [])
        
        close_pulls_and_issues_for_orgs()
        
        # Assertions to ensure the mocked function was called
        self.assertTrue(mock_close_pulls_and_issues.called)

if __name__ == '__main__':
    unittest.main()