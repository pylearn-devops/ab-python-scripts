import unittest
from unittest.mock import patch, MagicMock

class TestGetPolicyIds(unittest.TestCase):
    
    @patch('github.Github.get_repo')
    def test_get_policy_ids_success(self, mock_get_repo):
        # Arrange
        mock_repo = MagicMock()
        mock_contents = MagicMock()
        mock_contents.decoded_content = b"""
        # Policies
        Policy ID/21/Description
        Policy ID/22/Another Description
        Some text
        Policy ID/21/Another Policy/Description
        """
        mock_repo.get_contents.return_value = mock_contents
        mock_get_repo.return_value = mock_repo
        token = "fake_token"
        
        # Act
        result = get_policy_ids(token)
        
        # Assert
        expected_ids = ['Description', 'Another Description', 'Description']
        self.assertEqual(result, expected_ids)

    @patch('github.Github.get_repo')
    def test_get_policy_ids_no_matches(self, mock_get_repo):
        # Arrange
        mock_repo = MagicMock()
        mock_contents = MagicMock()
        mock_contents.decoded_content = b"""
        # Policies
        Some text without matching pattern
        """
        mock_repo.get_contents.return_value = mock_contents
        mock_get_repo.return_value = mock_repo
        token = "fake_token"
        
        # Act
        result = get_policy_ids(token)
        
        # Assert
        self.assertEqual(result, [])
        
    @patch('github.Github.get_repo')
    def test_get_policy_ids_github_exception(self, mock_get_repo):
        # Arrange
        mock_get_repo.side_effect = GithubException(404, "Not Found", None)
        token = "fake_token"
        
        # Act
        result = get_policy_ids(token)
        
        # Assert
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()