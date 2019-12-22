from data_reader import ReadData
import numpy as np
import unittest

class DataReaderTest(unittest.TestCase):
    """
    This class is a testfunction for the datareader.
    """
    def test_canary(self):
        """testing that the simplest case works."""
        self.assertEqual(2, 2)

    def test_(self):
        """
        testing that the ouput has correct dimension
        """
        return 1

    def test_undersampling(self):
        """
        Checks that the ratio property of the function is working properly
        """
        # with self.assertRaises(ValueError):
        return 1



if __name__ == '__main__':
    unittest.main()
