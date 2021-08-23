import numpy as np
import unittest, sys

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

"""
OMNI
"""


class OMNIReaderTest(unittest.TestCase):
    """
    This class is a testfunction for the magnetometer datareader.
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
        obj = ReadOMNIData()

        # testing properties
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.time
        with self.assertRaises(SyntaxError):
            obj.day_of_year
        with self.assertRaises(SyntaxError):
            obj.ACE_B_z
        with self.assertRaises(SyntaxError):
            obj.AE_index

        # testing printing
        with self.assertRaises(SyntaxError):
            obj.print_dataframe()
        with self.assertRaises(SyntaxError):
            obj.print_memory_usage()

    def test_known_example(self):
        """
        Testing know values from the OMNI_test data
        """
        n = 61
        obj = ReadOMNIData()
        obj.read_csv("data_reader_OMNI/example_OMNI.csv")
        # checking number of datapoints and sizes of arrays
        self.assertEqual(obj.datapoints, n)
        self.assertEqual(len(obj.day_of_year[0]), n)
        self.assertEqual(len(obj.time), n)
        # day and year check
        self.assertEqual(int(sum(obj.ACE_B_z)), -331)
        self.assertEqual(int(sum(obj.AE_index)), 20204)


if __name__ == "__main__":
    unittest.main()
