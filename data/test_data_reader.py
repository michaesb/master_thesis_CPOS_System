from data_reader import ReadData
import numpy as np
import unittest

class DataReaderTest(unittest.TestCase):
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
        obj = ReadData()
        #texsting displays
        with self.assertRaises(SyntaxError):
            obj.display_epochs()
        with self.assertRaises(SyntaxError):
            obj.display_location_satellite()
        with self.assertRaises(SyntaxError):
            obj.display_data()
        with self.assertRaises(SyntaxError):
            obj.display_epochs()
        with self.assertRaises(SyntaxError):
            obj.textdocument_version_display()
        with self.assertRaises(SyntaxError):
            obj.display_single_datapoint(0)
        with self.assertRaises(SyntaxError):
            obj.receiver_display()
        with self.assertRaises(SyntaxError):
            obj.display_date()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.epochs
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.satellite_Id
        with self.assertRaises(SyntaxError):
            obj.textdocument_version
        with self.assertRaises(SyntaxError):
            obj.datasizes
        with self.assertRaises(SyntaxError):
            obj.day_year
        #checking that reading files with error in them raises an error
        with self.assertRaises(ValueError):
            obj.read_textfile("data/example_data_ver_1_3_incorrect")
        obj1_1 = ReadData()
        with self.assertRaises(ValueError):
            obj1_1.read_textfile("data/example_data_ver_1_1_incorrect")

    def test_known_example1_1(self):
        """
        Testing for a known example with version 1.1. This include:
        *
        *the datacounter is equal 11 and equal to the sum of datasizes
        """
        #testing with version 1.1
        obj = ReadData()

        #checking the datacounter
        obj.read_textfile("data/example_data_ver_1_1")
        self.assertEqual(obj.datapoints, 11)
        self.assertEqual(np.sum(obj.datasizes),obj.datapoints)

    def test_known_example1_3(self):
        """
        testing with version 1.3. This include:
        *
        *the datacounter is equal 33 and equal to the sum of datasizes
        """
        obj = ReadData()

        #checking the datacounter
        obj.read_textfile("data/example_data_ver_1_3")
        self.assertEqual(obj.datapoints, 33)
        self.assertEqual(np.sum(obj.datasizes),obj.datapoints)


    def test_(self):
        """
        """
        obj = ReadData()
if __name__ == '__main__':
    unittest.main()
