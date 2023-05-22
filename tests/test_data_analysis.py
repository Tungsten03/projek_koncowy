import unittest
from unittest.mock import Mock, patch

from data_filter import data_analysis



class TestHighestMeasurement(unittest.TestCase):

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_highest_measurement(self, mock_select):
        # Define a mock measurement
        mock_measurement = Mock()
        mock_measurement.value = 100
        mock_measurement.date = '2023-01-01'

        mock_select.return_value.order_by.return_value.where.return_value.first.return_value = mock_measurement

        # Test the function
        result = data_analysis.highest_measurement(1)
        # Result should be '100 d:2023-01-01'
        self.assertEqual(result, '100 d:2023-01-01')

class TestLowestMeasurement(unittest.TestCase):

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_lowest_measurement(self, mock_select):
        # Define a mock measurement
        mock_measurement = data_analysis.sdb.Measurement()
        mock_measurement.value = 5
        mock_measurement.date = '2023-07-22'
        mock_select.return_value.order_by.return_value.where.return_value.first.return_value = mock_measurement

        result = data_analysis.lowest_measurement(1)
        self.assertEqual(result, '5 d:2023-07-22')




class TestAvgMeasurement(unittest.TestCase):
    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_avg_measurement(self, mock_measurement):
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
        # Mock empty measurement
        mock_measurement.return_value.where.return_value = []

        # Test the function
        result = data_analysis.avg_measurement(1)

        # Result should be 0.0
        self.assertEqual(result, 0.0)

    @patch.object(data_analysis.sdb.Measurement, 'select')
    def test_avg_measurement_single_measurement(self, mock_measurement):
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