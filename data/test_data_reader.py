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
        #checking that reading files with error in them raises an error
        with self.assertRaises(ValueError):
            obj.read_textfile("data/example_data_ver_1_3_incorrect")
        obj1_1 = ReadData()
        with self.assertRaises(ValueError):
            obj1_1.read_textfile("data/example_data_ver_1_1_incorrect")

    def test_datapoint_counter(self):
        """
        Testing that the total number of datapoints matched the sizes of
        each sprecified dataset size in the textfile.
        """
        #testing with version 1.1
        obj1_1 = ReadData()
        obj1_1.read_textfile("data/example_data_ver_1_1")
        self.assertEqual(np.sum(obj1_1.datasizes),obj1_1.datapoints)
        #testing with version 1.3
        obj1_3 = ReadData()
        obj1_3.read_textfile("data/example_data_ver_1_3")
        self.assertEqual(np.sum(obj1_3.datasizes),obj1_3.datapoints)


    def test_(self):
        """
        """
        obj = ReadData()
if __name__ == '__main__':
    unittest.main()
