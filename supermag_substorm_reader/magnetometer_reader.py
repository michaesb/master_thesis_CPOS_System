import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time as time_module
import sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
"""
MAGNETOMETER
"""
class ReadMagnetomerData():
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
        self.nr_datapoints = -1


    def read_csv(self,csv_file, verbose=False):
        """
        Reads the substorm event list from supermag
        """
        self.verbose = verbose
        self.nr_lines = sum(line[0]!="#" for line in open(csv_file)) #getting the number of lines
        self.nr_datapoints = self.nr_lines-1
        self.csv_file = csv_file
        if self.verbose:
            print("reading magnetometer data with ",
            self.nr_datapoints," datapoints");
            t1 = time_module.time()

        #opening the csv_file
        self.dataframe_pd = pd.read_csv(csv_file,)
        if verbose:
            t2 = time_module.time()
            print("pandas work time",t2-t1)
        #extracting arrays from the datasets
        self.date_UTC, Extent, self.receiver_name,\
        self.geo_long,self.geo_lat,\
        MAGON,MAGLAT,MLT,MCOLAT,\
        IGRF_DECL,SZA,\
        self.dbn_nez,self.dbe_nez,self.dbz_nez,\
        self.dbn_geo,self.dbe_geo,self.dbz_geo = self.dataframe_pd.to_numpy().T

        if verbose:
            t3 = time_module.time()
            print("assigning to numpy array",t3-t2)

        self.time_UTC = np.zeros_like(self.date_UTC)
        self.date = np.zeros_like(self.date_UTC)
        self.year = int(self.date_UTC[0].split("-")[0])

        for i, dt in enumerate(self.date_UTC):
            self.date[i], self.time_UTC[i] = dt.split("T")
        if verbose:
            t4 = time_module.time()
            print("pre time-conversion", t4-t3)
        self.time_UTC = self.time_converted()
        if verbose:
            t5 = time_module.time()
            print("after time-conversion", t5-t4)
            t6 = time_module.time()
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
        Changes the self.time_UTC from 60 number system to a 10 number system.
        """
        N = len(self.time_UTC)
        time = np.zeros(N)
        for i in range(N):
            h, m, s = self.time_UTC[i].split(":")
            time[i] = float(h)+ float(m)/60+ float(s)/3600
        return time

    @property
    def time(self):
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

    def receiver_specific_data(self, receiver_ID):
        """
        returns the data from a specific receiver
        """
        self.check_read_data()
        df = self.dataframe_pd
        df["Date_UTC"] = pd.to_datetime(df["Date_UTC"],
                                        format="%Y-%m-%dT%H:%M:%S")

        spec_receiver = df[df["IAGA"] == receiver_ID]

        r = pd.date_range(start=spec_receiver["Date_UTC"].min(), end=spec_receiver["Date_UTC"].max(), freq="1 min")

        spec_receiver = spec_receiver.set_index('Date_UTC').reindex(r).fillna(np.nan).rename_axis('Date_UTC').reset_index()

        print("hello there \n", spec_receiver.index)
        # date_UTC, Extent, receiver_name,\
        # geo_long,geo_lat,\
        # MAGON,MAGLAT,MLT,MCOLAT,\
        # IGRF_DECL,SZA,\
        # n_mag,e_mag,z_mag,\
        # n_geo,e_geo,z_geo = spec_receiver.to_numpy().T
        print(spec_receiver)
        
        date_UTC = spec_receiver["Date_UTC"].values
        geo_long,geo_lat = spec_receiver["GEOLON"], spec_receiver["GEOLAT"]
        n_mag,e_mag,z_mag = spec_receiver["dbn_nez"], spec_receiver["dbe_nez"],spec_receiver["dbz_nez"]
        n_geo,e_geo,z_geo = spec_receiver["dbn_geo"], spec_receiver["dbe_geo"], spec_receiver["dbz_geo"]
        return date_UTC, \
               geo_long,geo_lat,\
               n_mag,e_mag,z_mag,\
               n_geo,e_geo,z_geo


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
    obj = ReadMagnetomerData()
    obj.read_csv("example_magnetometer.csv",verbose=True)
    print(obj.print_dataframe())
    time,b,c,d,e,f,g,h,i = obj.receiver_specific_data("DON")
    print(time)
    # print("magnetic time", obj.magnetic_time)
    # print("day_of_year", obj.day_of_year)
