from data_reader_ROTI.ROTI_data_reader import ReadROTIData
import numpy as np
import unittest
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
        self.assertEqual(2, 2)

    def test_error_raises(self):
        """
        testing that the correct error is raised, when inporoperly used and
        given bad files. (Here we just test that there's not a missing number)
        """
        obj = ReadROTIData()
        #testing displays
        # with self.assertRaises(SyntaxError):
        #     obj.display_epochs()
        # with self.assertRaises(SyntaxError):
        #     obj.display_location_satellite()
        # with self.assertRaises(SyntaxError):
        #     obj.display_data()
        # with self.assertRaises(SyntaxError):
        #     obj.display_epochs()
        # with self.assertRaises(SyntaxError):
        #     obj.textdocument_version_display()
        # with self.assertRaises(SyntaxError):
        #     obj.receiver_display()
        # with self.assertRaises(SyntaxError):
        #     obj.display_date()
        # with self.assertRaises(SyntaxError):
        #     obj.time()
        #
        # #testing properties
        # with self.assertRaises(SyntaxError):
        #     obj.epochs
        # with self.assertRaises(SyntaxError):
        #     obj.datapoints
        # with self.assertRaises(SyntaxError):
        #     obj.satellite_Id
        # with self.assertRaises(SyntaxError):
        #     obj.textdocument_version
        # with self.assertRaises(SyntaxError):
        #     obj.datasizes
        # with self.assertRaises(SyntaxError):
        #     obj.day_year
        # with self.assertRaises(SyntaxError):
        #     obj.L2_data
        # with self.assertRaises(SyntaxError):
        #     obj.L1_data
        # with self.assertRaises(SyntaxError):
        #     obj.location
        # #checking that reading files with error in them raises an error
        # with self.assertRaises(ValueError):
        #     obj.read_textfile("data_reader/example_data_ver_1_3_incorrect.txt")
        # obj1_1 = ReadROTIData()


    def test_known_example_ver_1_3(self):
        """
        Testing with version 1.3. This include:
        *checking the day and year
        *the datacounter is equal 33 and equal to the sum of datasizes
        *Version check
        *The right number of satelitteId recorded
        """
        # obj = ReadROTIData()


if __name__ == '__main__':
    unittest.main()
