import numpy as np
import unittest, sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
"""
ROTI
"""

class NMEADataReaderTest(unittest.TestCase):
    """
    This class is a testfunction for the datareader.
    """
    def test_canary(self):
        """
        testing that the simplest case works.
        """
        self.assertEqual(2, 2)

    def test_error_raises(self):
        """
        testing that the correct error is raised, when inporoperly used and
        given bad files. (Here we just test that there's not a missing number)
        """
        obj = ReadNMEAData()

        #testing displays
        with self.assertRaises(SyntaxError):
            obj.display_date()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.time_period
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.day_year
        with self.assertRaises(SyntaxError):
            obj.time_m
        with self.assertRaises(SyntaxError):
            obj.day_year

    def test_known_example(self):
        """
        Testing know values from NMEA_test data
        """

        obj = ReadNMEAData()
        obj.read_textfile("data_reader_NMEA/example_textfile_NMEA.txt")
        #checking number of datapoints
        self.assertEqual(obj.datapoints,60)
        #day and year check
        self.assertEqual(obj.day_year[2],2015)
        self.assertEqual(obj.day_year[1],3)
        self.assertEqual(obj.day_year[0],17)
        #checking the time
        self.assertEqual(obj.time_m[0],0)
        self.assertEqual(obj.time_m[1],1)
        start, end = obj.time_period
        self.assertEqual(start[2],0)
        self.assertEqual(end[2],59)
        


if __name__ == '__main__':
    unittest.main()
