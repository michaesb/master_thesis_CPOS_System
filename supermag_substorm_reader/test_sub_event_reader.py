import numpy as np
import unittest, sys
from data_reader_ROTI.ROTI_data_reader import ReadROTIData
"""
ROTI
"""

class ROTIDataReaderTest(unittest.TestCase):
    """
    This class is a testfunction for the datareader.
    """
    def test_canary(self):
        """
        testing that the simplest case works.
        """
        self.assertEqual(2,2)

    def test_error_raises(self):
        """
        testing that the correct error is raised, when inporoperly used and
        given bad files. (Here we just test that there's not a missing number)
        """
        obj = ReadROTIData()

        #testing displays
        with self.assertRaises(SyntaxError):
            obj.display_date()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.day_of_year
        with self.assertRaises(SyntaxError):
            obj.dates_time
        with self.assertRaises(SyntaxError):
            obj.latitude
        with self.assertRaises(SyntaxError):
            obj.magnetic_time
        # with self.assertRaises(SyntaxError):
        #     obj.ROTI_Grid_data
        # with self.assertRaises(SyntaxError):
        #     obj.coordinates

    def test_known_example(self):
        """
        Testing know values from the ROTI_test data
        """

        obj = ReadSubstormEvent()
        obj.read_textfile("supermag_substorm_reader/example_sub_event.csv")
        #checking number of datapoints
        self.assertEqual(obj.datapoints,49)
        #day and year check
        self.assertEqual(obj.day_year[0],2018)

        #checking coordinates



if __name__ == '__main__':
    unittest.main()
