import numpy as np
import pandas as pd
import time, sys

sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
"""
Event list
"""
class ReadSubstormEvent():
    def __init__(self):
        """
        initializing variables and lists
        """
        #info about the file
        self.csv_file = False # name for the csv_file
        self.nr_lines = -1
        #datasets property
        self.date = None
        self.time_UTC = None

    def read_csv(self,csv_file, verbose=False):
        """
        Reads the substorm event list from supermag
        """
        self.verbose = verbose
        self.nr_lines = sum(1 for line in open(csv_file)) #getting the number of lines
        self.nr_datapoints = self.nr_lines-1
        self.csv_file = csv_file
        if self.verbose:
            print("reading substorm event list with " + \
            str(self.nr_datapoints)+" datapoints")
            t1 = time.time()

        #opening the csv_file
        datafile = pd.read_csv(csv_file)
        #extracting arrays from the datasets
        date_time, self.MLATitude, self.MLTime = datafile.to_numpy().T
        self.date = np.zeros_like(date_time)
        self.time_UTC = np.zeros_like(date_time)
        self.year = int(date_time[0].split("-")[0])
        for i, dt in enumerate(date_time):
            self.date[i], self.time_UTC[i] = dt.split(" ")
            self.MLATitude[i], self.MLTime[i] = float(self.MLATitude[i]), float(self.MLTime[i])
        if self.verbose:
            t2 = time.time()
            print("time taken to read = ","%g"%(t2-t1))


    def check_read_data(self):
        """
        A test for the funtions that returns data.
        This raises an error and exits, if the read_data function
        has not been used.
        """
        if not self.csv_file:
            raise SyntaxError("need to read the data first, using read_csv")
            exit()

    #properties returns value
    @property
    def datapoints(self):
        """
        returns the number of datapoints extracted from the file.
        """
        self.check_read_data()
        return self.nr_datapoints

    @property
    def dates_time(self):
        """
        returns an array of the times the substorm happened
        """
        self.check_read_data()
        hour = np.zeros(self.nr_datapoints); minutes = np.zeros(self.nr_datapoints);
        seconds = np.zeros(self.nr_datapoints);
        for i in range(len(self.time_UTC)):
            h, m, s = self.time_UTC[i].split(":")
            hour[i], minutes[i], seconds[i] = float(h), float(m), float(s)
        self.time_UTC = hour + minutes/60 + seconds/3600
        return self.time_UTC

    @property
    def latitude(self):
        """
        returns the number of datapoints extracted from the file.
        """
        self.check_read_data()
        return self.MLATitude

    @property
    def magnetic_time(self):
        """
        returns the number of datapoints extracted from the file.
        """
        self.check_read_data()
        return self.MLTime


    @property
    def day_of_year(self):
        """
        returns the day and year
        """
        self.check_read_data()
        return self.date, self.year

if __name__ == '__main__':
    obj = ReadSubstormEvent()
    obj.read_csv("example_sub_event.csv",verbose=True)
    print(obj.datapoints)
    # print("latitude", obj.latitude)
    print("dates time", obj.dates_time)
    # print("magnetic time", obj.magnetic_time)
    # print("day_of_year", obj.day_of_year)
