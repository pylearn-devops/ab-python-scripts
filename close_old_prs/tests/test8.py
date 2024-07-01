import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import logging
from src.close_stale_prs_issues import has_exempt_labels, close_pulls_and_issues
from src.constants import EXEMPT_LABELS, CLOSE_COMMENT

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
        self.mock_repo.get_pulls.return_value = [self.mock_item_without_exempt_label]
        self.mock_repo.get_issues.return_value = [self.mock_item_without_exempt_label]

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
        mock_org = mock_github_instance.get_organization.return_value
        mock_org.get_repos.return_value = [self.mock_repo]

        # Mock the get_secret function to return a dictionary with the token
        mock_get_secret.side_effect = lambda key: {"git_api_token": "mock_token"}[key]

        # Mock created_at date for items
        ignored_date = datetime(2023, 9, 30, tzinfo=timezone.utc)
        self.mock_item_without_exempt_label.created_at = datetime(2023, 6, 1, tzinfo=timezone.utc)
        self.mock_item_without_exempt_label.pull_request = None  # Ensure it's an issue, not a PR

        # Add the create_issue_comment and edit mocks
        self.mock_item_without_exempt_label.create_issue_comment = MagicMock()
        self.mock_item_without_exempt_label.edit = MagicMock()

        # Run the function
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues("mock_org")

        # Log the results
        print("Closed Count:", closed_count)
        print("Exempt PRs:", exempt_prs)
        print("Exempt Issues:", exempt_issues)

        # Assertions
        self.assertEqual(closed_count, 1)
        self.assertEqual(len(exempt_prs), 0)
        self.assertEqual(len(exempt_issues), 0)
        self.mock_item_without_exempt_label.create_issue_comment.assert_called_with(CLOSE_COMMENT)
        self.mock_item_without_exempt_label.edit.assert_called_with(state='closed')

if __name__ == '__main__':
    unittest.main()