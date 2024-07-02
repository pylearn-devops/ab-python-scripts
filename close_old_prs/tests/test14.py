import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Import the functions and any necessary modules from your script
from your_script import close_pulls_and_issues, close_pulls_and_issues_for_orgs

class TestGitHubPRsIssues(unittest.TestCase):

    @patch('your_script.Github')
    @patch('your_script.get_secret')
    def setUp(self, mock_get_secret, mock_github):
        # Set up mocks for secrets and GitHub API
        mock_get_secret.return_value = 'mock_secret_value'
        self.mock_github_instance = MagicMock()
        mock_github.return_value = self.mock_github_instance

        # Mock repository data
        self.mock_repo = MagicMock()
        self.mock_repo.name = "mock_repo"

        # Mock pull requests and issues
        self.mock_pr = MagicMock()
        self.mock_pr.created_at = datetime(2022, 1, 1, tzinfo=timezone.utc)
        self.mock_pr.labels = []
        self.mock_pr.number = 1
        self.mock_pr.title = "Test PR"
        self.mock_pr.user.login = "test_user"

        self.mock_issue = MagicMock()
        self.mock_issue.created_at = datetime(2022, 1, 1, tzinfo=timezone.utc)
        self.mock_issue.labels = []
        self.mock_issue.pull_request = None
        self.mock_issue.number = 1
        self.mock_issue.title = "Test Issue"
        self.mock_issue.user.login = "test_user"

        self.mock_repo.get_pulls.return_value = [self.mock_pr]
        self.mock_repo.get_issues.return_value = [self.mock_issue]

        self.mock_org = MagicMock()
        self.mock_org.get_repos.return_value = [self.mock_repo]

        self.mock_github_instance.get_organization.return_value = self.mock_org

    def test_close_pulls_and_issues(self):
        org_name = "mock_org"
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues(org_name)

        self.assertEqual(closed_count, 1)
        self.assertEqual(len(exempt_prs), 0)
        self.assertEqual(len(exempt_issues), 0)
        
        # Verify methods were called
        self.mock_repo.get_pulls.assert_called_once_with(state='open')
        self.mock_repo.get_issues.assert_called_once_with(state='open')

    def test_close_pulls_and_issues_for_orgs(self):
        closed_count, exempt_prs, exempt_issues = close_pulls_and_issues_for_orgs()

        self.assertEqual(closed_count, 1)
        self.assertEqual(len(exempt_prs), 0)
        self.assertEqual(len(exempt_issues), 0)

if __name__ == '__main__':
    unittest.main()