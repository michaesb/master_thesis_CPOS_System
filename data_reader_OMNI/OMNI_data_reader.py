import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numba import njit, prange
import time, sys

sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
"""
OMNI
"""
class ReadOMNIData():
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
        self.nr_datapoints = sum(line[0] != "#" for line in open(csv_file))
        self.csv_file = csv_file
        if self.verbose:
            print("reading OMNI data with " + \
            str(self.nr_datapoints)+" datapoints")
            t1 = time.time()

        #opening the csv_file
        self.dataframe_pd = pd.read_csv(csv_file,
                                        comment = "#")
                                        #na_values={'by': 9999.99,})

        if verbose:
            t2 = time.time()
            print("pandas work time",t2-t1)
        date_time,self.BZ,self.AE = self.dataframe_pd.to_numpy().T
        self.nr_datapoints = len(date_time)
        #remove comments at the end.
        self.year = int(date_time[0].split("-")[0])
        self.date = np.zeros_like(date_time)
        self.time_UTC = np.zeros(self.nr_datapoints)
        for i, dt in enumerate(date_time):
            self.date[i],temp = dt.split("T")
            self.time_UTC[i] = float(temp[:2])+ float(temp[3:5])/60
            if float(self.BZ[i]) == 9999.99:
                self.BZ[i] = np.nan
            else:
                self.BZ[i] = float(self.BZ[i])
            if float(self.AE[i]) >= 99999:
                self.AE[i] = np.nan
            else:
                self.AE[i] = float(self.AE[i])
        if verbose:
            t3 = time.time()
            print("convert to numpy array", t3-t2)
            t4 = time.time()
            print("time taken to read = ","%g"%(t4-t1))

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
    def time(self):
        """
        returns an array of the times axis
        """
        self.check_read_data()
        return self.time_UTC

    @property
    def AE_index(self):
        """
        Returns the geographic pole directions of the data of all receivers.
        """
        self.check_read_data()
        return self.AE

    @property
    def ACE_B_z(self):
        """
        Returns the magnetic pole directions of the data of all receivers.
        """
        self.check_read_data()

        return self.BZ

    @property
    def day_of_year(self):
        """
        returns the day and year
        """
        self.check_read_data()
        return self.date, self.year

    def print_memory_usage(self):
        """
        prints the memory usage of the dataframe.
        """
        self.check_read_data()
        print(self.dataframe_pd.memory_usage(index=False))

    def print_dataframe(self):
        """
        prints the dateframe from pandas.
        """
        self.check_read_data()
        print(self.dataframe_pd)


if __name__ == '__main__':
    obj = ReadOMNIData()
    obj.read_csv("example_OMNI.csv",verbose = True)
    obj.print_dataframe()
    print("day_of_year", obj.day_of_year)
