import numpy as np
import unittest, sys
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData

"""
MAGNETOMETER
"""

class MagnetomerReaderTest(unittest.TestCase):
    """
    This class is a testfunction for the magnetometer datareader.
    """
    def test_canary(self):
        """
        testing that the simplest case works.
        """
        self.assertEqual(2,2)

    def test_error_raises(self):
        """
        testing that the correct error is raised, when improperly used.
        """
        obj = ReadMagnetomerData()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.time
        with self.assertRaises(SyntaxError):
            obj.day_of_year
        with self.assertRaises(SyntaxError):
            obj.mag_flux_current
        with self.assertRaises(SyntaxError):
            obj.geo_flux_current

        #testing printing
        with self.assertRaises(SyntaxError):
            obj.print_dataframe()
        with self.assertRaises(SyntaxError):
            obj.print_memory_usage()

        #extra
        with self.assertRaises(SyntaxError):
            obj.receiver_specific_data("DON")


    def test_known_example(self):
        """
        Testing know values from the magnetometer_test data
        """
        n = 143
        obj = ReadMagnetomerData()
        obj.read_csv("supermag_substorm_reader/example_magnetometer.csv")
        #checking number of datapoints and sizes of arrays
        self.assertEqual(obj.datapoints,n)
        self.assertEqual(len(obj.day_of_year[0]),n)
        self.assertEqual(len(obj.time),n)
        #day and year check
        self.assertEqual(int(sum(obj.mag_flux_current[0])),-15722)
        self.assertEqual(int(sum(obj.geo_flux_current[0])),-17057)

        #specific receivers
        a,b,c,d,e,f,g,h,i,j =\
        obj.receiver_specific_data("DON")
        totalsum = len(a)+ len(b)+len(c)+ len(d) + len(e) + len(f) + len(g) + \
                    len(h)+ len(i) + len(j)
        self.assertEqual(totalsum, 110)


if __name__ == '__main__':
    unittest.main()
