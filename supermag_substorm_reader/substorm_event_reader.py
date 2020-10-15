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
        self.textfile = False # name for the textfile
        self.year = -1 #which year the data is recorded
        self.day = -1  #which day the data is recorded
        self.nr_lines = -1
        #datasets property
        #time
        self.start_time = [] # hour minute second
        self.end_time =  [] # hour minute second

    def read_textfile(self,textfile, verbose=False):
        """
        Reads the substorm event list from supermag
        """
        self.verbose = verbose
        self.nr_lines = sum(1 for line in open(textfile)) #getting the number of lines
        self.nr_datapoints = self.nr_lines-1
        self.textfile = textfile
        if self.verbose:
            count = 0
            print("reading substorm event list with " + \
            str(self.nr_datapoints)+" datapoints")
            t1 = time.time()
        #opening the textfile
        df = pd.read_csv(str(textfile))


        date, time_UTC, MLATitude, MLTime  =  df.to_numpy()
        if self.verbose:
            print("longitude:",self.coordinates[0])
            print("latitude:",self.coordinates[1])
            t2 = time.time()
            print("time taken to read = ","%g"%(t2-t1))


    def check_read_data(self):
        """
        A test for the funtions that returns data.
        This raises an error and exits, if the read_data function
        has not been used.
        """
        if not self.textfile:
            raise SyntaxError("need to read the data first, using read_textfile")
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
    def time_period(self):
        """
        returns the list of the times the data was retrived
        """
        self.check_read_data()
        return self.start_time,self.end_time

    @property
    def time(self):
        """
        returns the time from the start of the data and to the end data
        This assumes that it's continous and there are 5 minutes in between the
        points
        """
        self.check_read_data()
        hours = self.end_time[0]-self.start_time[0]
        minutes = self.end_time[1]-self.start_time[1]
        duration = minutes+ hours*60
        t = np.arange(self.start_time[1],self.start_time[1]+duration+5,5)
        #added plus five so it would create the final point as well.
        return t


if __name__ == '__main__':
    obj = ReadSubstormEvent()
    obj.read_textfile("example_sub_event.csv")
    print(obj.datapoints)
