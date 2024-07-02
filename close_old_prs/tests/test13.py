import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import logging
from src.close_stale_prs_issues import close_pulls_and_issues
from src.constants import CLOSE_COMMENT

class TestCloseStalePrsIssues(unittest.TestCase):

    @patch('src.close_stale_prs_issues.get_secret')
    @patch('src.close_stale_prs_issues.Github')
    @patch('src.close_stale_prs_issues.datetime')
    def test_close_single_issue(self, mock_datetime, mock_github, mock_get_secret):
        # Mock datetime to return a fixed current date
        mock_datetime.now.return_value = datetime(2024, 6, 30, tzinfo=timezone.utc)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mocking GitHub token and organization details
        mock_github_instance = mock_github.return_value
        mock_org = mock_github_instance.get_organization.return_value
        mock_repo = MagicMock()
        mock_org.get_repos.return_value = [mock_repo]

        # Mock a single issue
        mock_issue = MagicMock()
        mock_issue.labels = []
        mock_issue.number = 123
        mock_issue.title = "Mock Issue"
        mock_issue.user.login = "mockuser"
        mock_issue.created_at = datetime(2023, 6, 1, tzinfo=timezone.utc)
        mock_issue.pull_request = None
        mock_issue.create_comment = MagicMock()
        mock_issue.edit = MagicMock()

        mock_repo.get_pulls.return_value = []
        mock_repo.get_issues.return_value = [mock_issue]

        # Mock the get_secret function to return a dictionary with the token
        mock_get_secret.side_effect = lambda key: {"git_api_token": "mock_token"}[key]

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
        mock_issue.create_comment.assert_called_with(CLOSE_COMMENT)
        mock_issue.edit.assert_called_with(state='closed')

if __name__ == '__main__':
    unittest.main()