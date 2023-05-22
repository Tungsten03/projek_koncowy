import unittest
from unittest.mock import Mock, patch
import requests

from data_filter import localize


class TestCheckServer(unittest.TestCase):

    @patch('requests.head')
    def test_server_available(self, mock_head):
        # Define a mock response with status code 200
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        # The server should be available
        self.assertTrue(localize.check_server())

    @patch('requests.head')
    def test_server_unavailable(self, mock_head):
        # Define a mock response with status code other than 200
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        # The server should be unavailable
        self.assertFalse(localize.check_server())

    @patch('requests.head')
    def test_connection_error(self, mock_head):
        # Simulate a ConnectionError
        mock_head.side_effect = requests.ConnectionError()

        # The server should be unavailable
        self.assertFalse(localize.check_server())


if __name__ == '__main__':
    unittest.main()
