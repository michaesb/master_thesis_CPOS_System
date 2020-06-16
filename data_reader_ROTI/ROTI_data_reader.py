import numpy as np
import time, sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
"""
ROTI
"""
class ReadROTIData():
    def __init__(self):
        """
        initializing variables and lists
        """
        #info about the file
        self.textfile = False # name for the textfile
        self.version_number = -1  #version of the file format
        self.version = "No textdocument has been read" # version line for printing
        self.receiver = "No textdocument has been read" # receiver type for printing
        self.year = -1 #which year the data is recorded
        self.day_of_year = -1  #which day the data is recorded
        self.nr_lines = -1
        #lists of info
        self._data = [] # nested list of all the data unfiltered
        self._datasizes = [] #the sizes of each epoch
        #grid information
        self.ion_height =-1 #km. the ionospheric altitude.
        self.ROTI_deg = -1 #degrees. Elevation cutoff for ROTI
        self.ROTI_Ground_deg = -1 #degrees. Elevation cutoff for ROTI Ground

        #time
        self.start_time = [] # hour minute second
        self.end_time =  [] # hour minute second

    def read_textfile(self,textfile, verbose=False):
        """
        read textfile specified and selects the
        right textfile_reader based on what version the texfile is. Also reads
        the specifications for the for the data recording.
        """
        self.verbose = verbose
        self.nr_lines = sum(1 for line in open(textfile)) #getting the number of lines
        self.textfile = textfile
        with open(textfile, 'r') as infile:
            #extracting information from the comments
            nr_comments_read = 0
            for line in infile:
                line = line.split()
                if len(line)==0:
                    continue
                nr_comments_read+=1
                if nr_comments_read ==13:
                    self.ion_height = line[2] #
                if nr_comments_read ==14:
                    self.ROTI_deg = line[8]
                if nr_comments_read ==15:
                    self.ROTI_Ground_deg = line[8]
                if line[0] == "<EndOfComments>":
                     break
            #extracting grid information
            for line in infile:
                line = line.split()
                if len(line)==0:
                    continue
                nr_comments_read+=1


                if line[0] == "<EndOfHeader>":
                    break


    def check_read_data(self):
        """
        A test for the funtions that returns data.
        This raises an error and exits, if the read_data function
        has not been used.
        """
        if not self.textfile:
            raise SyntaxError("need to read the data first, using read_textfile")
            exit()

    @property
    def datapoints(self):
        """
        returns the number of datapoints extracted from the file.
        """
        self.check_read_data()
        return self.nr_datapoints

    @property
    def datasizes(self):
        """
        returns the datasizes in the textfile
        """
        self.check_read_data()
        return np.array(self._datasizes)


    @property
    def epochs(self):
        """
        returns the list of the times the data was retrived
        """
        self.check_read_data()
        return np.array(self._epochs[:])


    def time(self, unit=0):
        """
        returns the time from the start of the data and to the end data
        This assumes that it's continous and gives multiple output based on the
        parameter unit. unit=0 gives seconds, unit =1 gives minutes, unit = 2
        gives hours.
        """
        self.check_read_data()
        hours = self.end_time[0]-self.start_time[0]
        minutes = self.end_time[1]-self.start_time[1]
        seconds = self.end_time[2]-self.start_time[2]
        if unit==0:
            duration = seconds + minutes*60 +hours*3600
        if unit ==1:
            duration = seconds/60. + minutes+ hours*60
        if unit==2:
            duration = seconds/3600 + minutes/60 + hours
        self.check_read_data()
        n = len(self._S4_L1)
        t = np.linspace(self.start_time[2-unit],self.start_time[2-unit]+duration,n)
        print(t, len(t))
        return t


    @property
    def day_year(self):
        """
        returns of the day and year
        """
        self.check_read_data()
        return self.day_of_year, self.year



    def display_date(self):
        """
        displays the year and which day of the year
        """
        self.check_read_data()
        print("year: ",self.year," day: ", self.day_of_year )




if __name__ == '__main__':

    obj = ReadROTIData()
    obj.read_textfile("example_textfile_ROTI.txt")
