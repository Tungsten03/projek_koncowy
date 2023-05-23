"""
Unit tests for the data_analysis module.
"""


import unittest
from unittest.mock import Mock, patch
from data_filter import data_analysis



class TestHighestMeasurement(unittest.TestCase):

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_highest_measurement(self, mock_select):
        """
        Test for the highest_measurement function.

        Verifies a simple case by mocking a Measurement model and select method. It defines a mock
        measurement with specific value and date. Function is called with a station ID and results are compared.
        """
        # Define a mock measurement
        mock_measurement = Mock()
        mock_measurement.value = 100
        mock_measurement.date = '2023-01-01'
        # Configure mock_select to return mock_measurement
        mock_select.return_value.order_by.return_value.where.return_value.first.return_value = mock_measurement

        # Test the function
        result = data_analysis.highest_measurement(1)
        # Result should be '100 d:2023-01-01'
        self.assertEqual(result, '100 d:2023-01-01')

class TestLowestMeasurement(unittest.TestCase):

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_lowest_measurement(self, mock_select):
        """
        Test for the lowest_measurement function.

        Verifies a simple case by mocking a Measurement model and select method. It defines a mock
        measurement with specific value and date. Function is called with a station ID and results are compared.
        """
        # Define mock measurement
        mock_measurement = Mock()
        mock_measurement.value = 5
        mock_measurement.date = '2023-07-22'

        # Configure mock_select to return mock_measurement
        mock_select.return_value.order_by.return_value.where.return_value.first.return_value = mock_measurement

        result = data_analysis.lowest_measurement(1)
        self.assertEqual(result, '5 d:2023-07-22')


class TestAvgMeasurement(unittest.TestCase):
    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_avg_measurement(self, mock_measurement):
        """
        Test for the avg_measurement function.

        Verifies a simple case by mocking a Measurement model and select method. It mocks a list of measurements
        with specific values. The function is called with a station ID, and the expected result is compared
        with the actual result.
        """
        # Mock Measurement data
        mock_measurement.return_value.where.return_value = [
            data_analysis.sdb.Measurement(value=1),
            data_analysis.sdb.Measurement(value=2),
            data_analysis.sdb.Measurement(value=3)
        ]

        # Test the function
        result = data_analysis.avg_measurement(1)

        # Result should be 2.0
        self.assertEqual(result, 2.0)

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_avg_measurement_empty(self, mock_measurement):
        """
        Test the 'avg_measurement' function when there are no measurements.

        This test case verifies that the 'avg_measurement' function returns 0.0 when there are no measurements available.

        :param mock_measurement: Mock object representing the patched 'Measurement.select' method.
        """
        # Mock empty measurement
        mock_measurement.return_value.where.return_value = []

        # Test the function
        result = data_analysis.avg_measurement(1)

        # Result should be 0.0
        self.assertEqual(result, 0.0)

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_avg_measurement_single_measurement(self, mock_measurement):
        """
        Test the 'avg_measurement' function with a single measurement.

        This test case verifies that the 'avg_measurement' function returns the correct average value
        when there is only one measurement available.

        :param mock_measurement: Mock object representing the patched 'Measurement.select' method.
        """
        # Mock single measurement data
        mock_measurement.return_value.where.return_value = [
            data_analysis.sdb.Measurement(value=5)
        ]

        # Test the function
        result = data_analysis.avg_measurement(1)

        # Result should be 5.0
        self.assertEqual(result, 5.0)

if __name__ == '__main__':
    unittest.main()