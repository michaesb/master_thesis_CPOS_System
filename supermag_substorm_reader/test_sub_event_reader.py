import numpy as np
import unittest, sys
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
"""
ROTI
"""

class SubstormDataReaderTest(unittest.TestCase):
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
        obj = ReadSubstormEvent()

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

    def test_known_example(self):
        """
        Testing know values from the ROTI_test data
        """
        n = 49
        obj = ReadSubstormEvent()
        obj.read_csv("supermag_substorm_reader/example_sub_event.csv")
        #checking number of datapoints and sizes of arrays
        self.assertEqual(obj.datapoints,n)
        self.assertEqual(len(obj.day_of_year[0]),n)
        #day and year check
        self.assertEqual(int(sum(obj.magnetic_time)),680)
        self.assertEqual(int(sum(obj.latitude)),3396)


if __name__ == '__main__':
    unittest.main()
