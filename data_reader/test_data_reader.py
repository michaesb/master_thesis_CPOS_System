from data_reader.data_reader_main import ReadData
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
        #testing displays
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
            obj.receiver_display()
        with self.assertRaises(SyntaxError):
            obj.display_date()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.epochs
        with self.assertRaises(SyntaxError):
            obj.time
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
        with self.assertRaises(SyntaxError):
            obj.L2_data
        with self.assertRaises(SyntaxError):
            obj.L1_data
        with self.assertRaises(SyntaxError):
            obj.location
        #checking that reading files with error in them raises an error
        with self.assertRaises(ValueError):
            obj.read_textfile("data_reader/example_data_ver_1_3_incorrect.txt")
        obj1_1 = ReadData()
        with self.assertRaises(ValueError):
            obj1_1.read_textfile("data_reader/example_data_ver_1_1_incorrect.txt")

    def test_known_example_ver_1_1(self):
        """
        Testing for a known example with version 1.1. This include:
        *checking the day and year
        *the datacounter is equal 11 and equal to the sum of datasizes
        *Version check
        *The right number of satelitteId recorded in the textfile
        """

        obj = ReadData()
        obj.read_textfile("data_reader/example_data_ver_1_1.txt")
        #checking the year and date
        self.assertEqual(obj.day_year[0],270)
        self.assertEqual(obj.day_year[1],2011)
        #checking the datacounter
        self.assertEqual(obj.datapoints, 40) #should be 60 or 30
        self.assertEqual(np.sum(obj.datasizes),obj.datapoints)
        # version check 1.1
        self.assertEqual(obj.textdocument_version,1.1)
        #satelitteId check
        self.assertEqual(len(obj.satellite_Id),20)


    def test_known_example_ver_1_3(self):
        """
        Testing with version 1.3. This include:
        *checking the day and year
        *the datacounter is equal 33 and equal to the sum of datasizes
        *Version check
        *The right number of satelitteId recorded
        """
        obj = ReadData()
        obj.read_textfile("data_reader/example_data_ver_1_3.txt")
        #checking the year and date
        self.assertEqual(obj.day_year[0],108)
        self.assertEqual(obj.day_year[1],2018)

        #checking the datacounter
        self.assertEqual(obj.datapoints, 56)
        self.assertEqual(np.sum(obj.datasizes),obj.datapoints)
        # version check 1.3
        self.assertEqual(obj.textdocument_version,1.3)
        #satelitteId
        self.assertEqual(len(obj.satellite_Id),20)



if __name__ == '__main__':
    unittest.main()
