import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import logging
from src.close_stale_prs_issues import has_exempt_labels, close_pulls_and_issues, close_pulls_and_issues_for_orgs
from src.constants import EXEMPT_LABELS, GITHUB_URL, GITHUB_ORGANIZATIONS, CLOSE_COMMENT

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

        # Set up logging to capture output for assertions
        logger = logging.getLogger('src.close_stale_prs_issues')
        logger.setLevel(logging.DEBUG)
        log_capture = logging.StreamHandler()
        log_capture.setLevel(logging.DEBUG)
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_capture.setFormatter(log_formatter)
        logger.addHandler(log_capture)

        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues("mock_org")

        # Assertions
        self.assertEqual(closed_count, 1)
        self.assertEqual(len(exempt_prs), 1)
        self.assertEqual(len(exempt_issues), 0)
        self.mock_item_without_exempt_label.create_issue_comment.assert_called_with(CLOSE_COMMENT)
        self.mock_item_without_exempt_label.edit.assert_called_with(state='closed')

        # Check log output
        log_capture.flush()
        log_output = log_capture.stream.getvalue()
        print(log_output)

        logger.removeHandler(log_capture)
    
    @patch('src.close_stale_prs_issues.close_pulls_and_issues')
    @patch('src.close_stale_prs_issues.get_secret')
    def test_close_pulls_and_issues_for_orgs(self, mock_get_secret, mock_close_pulls_and_issues):
        # Mocking the close_pulls_and_issues function
        mock_close_pulls_and_issues.return_value = (1, [], [])
        
        # Mock the get_secret function to return a dictionary with the token
        mock_get_secret.side_effect = lambda key: {"git_api_token": "mock_token"}[key]

        close_pulls_and_issues_for_orgs()
        
        # Assertions to ensure the mocked function was called
        self.assertTrue(mock_close_pulls_and_issues.called)

if __name__ == '__main__':
    unittest.main()