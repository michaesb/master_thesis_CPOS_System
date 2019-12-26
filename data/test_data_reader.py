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

    def test_textdocument(self):
        """
        testing that the correct error is raised, when inporoperly handled
        """
        obj = ReadData()
        with self.assertRaises(SyntaxError):
            obj.display_epochs()
        with self.assertRaises(ValueError):
            obj.read_textfile("data/example_incorrect_data")


    def test_undersampling(self):
        """
        Checks that the ratio property of the function is working properly
        """
        obj = ReadData()
        obj.read_textfile("data/example_data")






if __name__ == '__main__':
    unittest.main()
