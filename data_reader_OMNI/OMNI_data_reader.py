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
        self.nr_datapoints = self.nr_lines-44
        self.csv_file = csv_file
        if self.verbose:
            print("reading OMNI data with " + \
            str(self.nr_datapoints)+" datapoints")
            t1 = time.time()

        #opening the csv_file
        self.dataframe_pd = pd.read_csv(csv_file)
        if verbose:
            t2 = time.time()
            print("pandas work time",t2-t1)
        #extracting arrays from the datasets
        self.dataframe_matrix = self.dataframe_pd.to_numpy().T

        self.date_UTC, Extent, self.receiver_name,\
        self.geo_long,self.geo_lat,\
        MAGON,MAGLAT,MLT,MCOLAT,\
        IGRF_DECL,SZA,\
        self.dbn_nez,self.dbe_nez,self.dbz_nez,\
        self.dbn_geo,self.dbe_geo,self.dbz_geo = self.dataframe_pd.to_numpy().T
        if verbose:
            t3 = time.time()
            print("assigning to numpy array",t3-t2)
        self.time_UTC = np.zeros_like(self.date_UTC)
        self.date = np.zeros_like(self.date_UTC)
        self.year = int(self.date_UTC[0].split("-")[0])
        for i, dt in enumerate(self.date_UTC):
            self.date[i], self.time_UTC[i] = dt.split("T")
        if verbose:
            t4 = time.time()
            print("pre time-conversion", t4-t3)
        self.time_UTC = self.time_converted()
        if verbose:
            t5 = time.time()
            print("after time-conversion", t5-t4)
            t6 = time.time()
            print("time taken to read = ","%g"%(t6-t1))

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


    def time_converted(self,):
        """
        changes the self.time_UTC from 60 number system to 10 number system.
        """
        N = len(self.time_UTC)
        time = np.zeros(N)
        for i in prange(N):
            h, m, s = self.time_UTC[i].split(":")
            time[i] = float(h)+ float(m)/60+ float(s)/3600
        return time

    @property
    def time_(self):
        """
        returns an array of the times the substorm happened
        """
        self.check_read_data()
        return self.time_UTC

    @property
    def geo_flux_current(self):
        """
        Returns the geographic pole directions of the data of all receivers.
        """
        self.check_read_data()
        return self.dbn_geo,self.dbe_geo,self.dbz_geo

    @property
    def mag_flux_current(self):
        """
        Returns the magnetic pole directions of the data of all receivers.
        """
        self.check_read_data()
        return self.dbn_nez,self.dbe_nez,self.dbz_nez,

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


if __name__ == '__main__':
    obj = ReadOMNIData()
    # print("magnetic time", obj.magnetic_time)
    # print("day_of_year", obj.day_of_year)
