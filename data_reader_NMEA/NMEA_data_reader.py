import numpy as np
import time, sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
"""
NMEA
"""
class ReadNMEAData():
    def __init__(self):
        """
        initializing variables and lists
        """
        #info about the file
        self.textfile = False # name for the textfile
        self.date = "False"
        self.year = -1 #which year the data is recorded
        self.day = -1  #which day the data is recorded
        self.nr_lines = -1
        #time
        self.start_time = [] # hour minute second
        self.end_time =  [] # hour minute second
        #data
        self.nr_datapoints = 0

    def read_textfile(self,textfile, verbose=False):
        """
        read textfile specified and selects the
        right textfile_reader based on what version the texfile is. Also reads
        the specifications for the for the data recording.
        """
        self.verbose = verbose
        self.nr_lines = sum(1 for line in open(textfile)) #getting the number of lines
        self.textfile = textfile
        if self.verbose:
            print("reading NMEA textfile with " +str(self.nr_lines)+" lines")
            t1 = time.time()
        count_line = 0
        #opening the textfile
        with open(textfile, 'r') as infile:
            for line in infile:

                self.date, self.time_temp, self.data_line = line.split()
                if count_line ==0:
                    self.start_time = float(self.time_temp[0:1]),\
                                      float(self.time_temp[3:4]), \
                                      float(self.time_temp[6:7])
                #print(self.date, self.time_temp, self.data_line)
                count_line+=1
                self.nr_datapoints+=1
        self.end_time = float(self.time_temp[0:2]),\
                        float(self.time_temp[3:5]), \
                        float(self.time_temp[6:8])
        if self.verbose:
            t2 = time.time()
            print("time taken to read = %g"%(t2-t1))


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
        return self.start_time, self.end_time

    @property
    def time_m(self):
        """
        returns the time from the start of the data and to the end data
        This assumes that it's continous and there are 5 minutes in between the
        points
        """
        self.check_read_data()
        hours = self.end_time[0]-self.start_time[0]
        minutes = self.end_time[1]-self.start_time[1]
        seconds = self.end_time[2]-self.start_time[2]
        print(hours,minutes,seconds)
        duration = np.ceil(minutes+ hours*60. +seconds/60.)
        print(duration)
        t = np.linspace(self.start_time[1],self.start_time[1]+duration,\
                        int(self.nr_datapoints/60.)+1)
        return t

    @property
    def day_year(self):
        """
        returns of the day and year
        """
        self.check_read_data()
        self.year,self.month, self.day = float(self.date[0:4]),\
                                         float(self.date[5:7]),\
                                         float(self.date[8:10])
        return self.day, self.month, self.year

    #printing values or tables
    def display_date(self):
        """
        displays the year and which day of the year
        """
        self.check_read_data()
        self.year,self.month, self.day = float(self.date[0:4]),\
                                         float(self.date[5:7]),\
                                         float(self.date[8:10])
        print("year: ",self.year," day: ", self.day)

if __name__ == '__main__':
    obj = ReadNMEAData()
    obj.read_textfile("example_textfile_NMEA.txt")
    print(obj.datapoints)
    print(obj.day_year)
    print(obj.time_period)
    print(obj.time_m)
