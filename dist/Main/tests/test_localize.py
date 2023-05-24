import unittest
from unittest.mock import Mock, patch
import requests
from data_filter import localize


class TestCheckServer(unittest.TestCase):

    @patch('requests.head')
    def test_server_available(self, mock_head):
        """
        Test the 'check_server' function when the server is available.

        This test case verifies that the 'check_server' function returns True when the server
        responds status code 200.

        :param mock_head: Mock object representing the patched 'requests.head' function.
        """
        # Define a mock response with status code 200
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        # The server should be available
        self.assertTrue(localize.check_server())

    @patch('requests.head')
    def test_server_unavailable(self, mock_head):
        """
        Test the 'check_server' function when the server is unavailable.

        This test case verifies that the 'check_server' function returns False when the server responds
        status code other than 200.

        :param mock_head: Mock object representing the patched 'requests.head' function.
        """
        # Define a mock response with status code other than 200
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        # The server should be unavailable
        self.assertFalse(localize.check_server())

    @patch('requests.head')
    def test_connection_error(self, mock_head):
        """
        Test the 'check_server' function when a ConnectionError occurs.

        This test case verifies that the 'check_server' function returns False when a ConnectionError is raised.

        :param mock_head: Mock object representing the patched 'requests.head' function.
        """
        # Simulate a ConnectionError
        mock_head.side_effect = requests.ConnectionError()

        # The server should be unavailable
        self.assertFalse(localize.check_server())


if __name__ == '__main__':
    unittest.main()
