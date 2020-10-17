import numpy as np
import unittest, sys
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
"""
NMEA
"""

class NMEADataReaderTest(unittest.TestCase):
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
        testing that the correct error is raised, when inporoperly used.
        """
        obj = ReadNMEAData()

        #testing displays
        with self.assertRaises(SyntaxError):
            obj.display_date()
        with self.assertRaises(SyntaxError):
            obj.display_coordinates_type()
        with self.assertRaises(SyntaxError):
            obj.display_coordinates()
        with self.assertRaises(SyntaxError):
            obj.display_GPS_indicator()

        #testing properties
        with self.assertRaises(SyntaxError):
            obj.time_period
        with self.assertRaises(SyntaxError):
            obj.datapoints
        with self.assertRaises(SyntaxError):
            obj.day_year
        with self.assertRaises(SyntaxError):
            obj.time_m
        with self.assertRaises(SyntaxError):
            obj.time_h
        with self.assertRaises(SyntaxError):
            obj.day_year
        with self.assertRaises(SyntaxError):
            obj.talker_identifier
        with self.assertRaises(SyntaxError):
            obj.coordinates
        with self.assertRaises(SyntaxError):
            obj.qualities_indicator
        with self.assertRaises(SyntaxError):
            obj.nr_satellites
        with self.assertRaises(SyntaxError):
            obj.horizontal_dil_of_pos
        with self.assertRaises(SyntaxError):
            obj.geoidal_seperation
        with self.assertRaises(SyntaxError):
            obj.station_ID
        with self.assertRaises(SyntaxError):
            obj.track_4

    def test_known_example(self):
        """
        Testing know values from NMEA_test data
        """

        """
        Testing the time aspects of the Class
        """
        obj = ReadNMEAData()
        obj.read_textfile("data_reader_NMEA/example_textfile_NMEA.txt")
        #checking number of datapoints
        self.assertEqual(obj.datapoints,(40,60))
        #day and year check
        self.assertEqual(obj.day_year[2],2015)
        self.assertEqual(obj.day_year[1],3)
        self.assertEqual(obj.day_year[0],17)
        #checking the time
        self.assertEqual(obj.time_m[0],0)
        start, end = obj.time_period
        self.assertEqual(start[0]+start[1]+start[2],0)
        self.assertEqual(end[0]+end[1]+end[2],59)
        self.assertEqual(sum(obj.track_4),46)


if __name__ == '__main__':
    unittest.main()
