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
            obj.time_period
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.day_year
        with self.assertRaises(SyntaxError):
            obj.time
        with self.assertRaises(SyntaxError):
            obj.day_year
        with self.assertRaises(SyntaxError):
            obj.ROTI_data
        with self.assertRaises(SyntaxError):
            obj.ROTI_Grid_data
        with self.assertRaises(SyntaxError):
            obj.coordinates

    def test_known_example(self):
        """
        Testing know values from the ROTI_test data
        """

        obj = ReadROTIData()
        obj.read_textfile("data_reader_ROTI/example_textfile_ROTI.txt")
        #checking number of datapoints
        self.assertEqual(obj.datapoints,6324)
        self.assertEqual(obj.datasets,2)
        #day and year check
        self.assertEqual(obj.day_year[0],17)
        self.assertEqual(obj.day_year[1],2015)

        #checking the time
        self.assertEqual(obj.time[0],0)
        self.assertEqual(obj.time[1],5)
        start, end = obj.time_period
        self.assertEqual(start,[0,0,0])
        self.assertEqual(end,[0,5,0])
        #checking coordinates
        latitude,longitude = obj.coordinates
        self.assertEqual(latitude[0],-10)
        self.assertEqual(latitude[1],40)
        self.assertEqual(latitude[2],1) #interval check
        self.assertEqual(longitude[0],50)
        self.assertEqual(longitude[1],80)
        self.assertEqual(longitude[2],1) #interval check



if __name__ == '__main__':
    unittest.main()
