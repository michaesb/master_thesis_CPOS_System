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
        self.year = -1 #which year the data is recorded
        self.day = -1  #which day the data is recorded
        self.nr_lines = -1
        #grid information
        self.ion_height =-1 #km. the ionospheric altitude.
        self.ROTI_deg = -1 #degrees. Elevation cutoff for ROTI
        self.ROTI_Ground_deg = -1 #degrees. Elevation cutoff for ROTI Ground
        self.longitude = [] #from, to, interval.
        self.latitude = [] #from, to, interval.
        self.longitude_axis_size = -1
        self.latitude_axis_size = -1
        #datasets property
        self.nr_datasets = 0
        self.nr_datapoints = 0
        self.nr_ROTI_ion_sets = 0
        self.nr_ROTI_grid_sets = 0
        self.unit = -1
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
        if self.verbose:
            count = 0
            print("reading ROTI textfile with " +str(self.nr_lines)+" lines")
            t1 = time.time()
        #opening the textfile
        with open(textfile, 'r') as infile:
             #extracting information from the comments
            self.read_comments(infile)

            #extracting grid information
            self.read_grid(infile)
            #creating the empty grid matrix
            self.create_grid()
            #Reading the data
            for line in infile:
                line = line.split()
                if len(line)==0: #ignoring empty lines
                    continue
                #recording the time from the data
                if line[0] == "<StartOfEpoch>":
                    self.nr_datasets +=1
                    #getting date and time
                    self.date = [float(i) for i in infile.readline().split()]
                    self.year = self.date[0]; self.month=self.date[1]
                    self.day = self.date[2]
                    if len(self.start_time)==0:
                        self.start_time= [self.date[3],self.date[4],self.date[5]]
                    self.end_time = [self.date[3],self.date[4],self.date[5]]
                #reading the data
                if line[0] == "<StartOfVariable>":
                    measure_type = infile.readline().split()[0]
                    if measure_type=="ROTI":
                        self.read_ROTI_ion(infile)
                    elif measure_type=="ROTI_Ground":
                        self.read_ROTI_Grid(infile)
                    else:
                        raise TypeError("Unknown measurement type used")
                    self.nr_datasets +=1

        if self.verbose:
            print("longitude:",self.coordinates[0])
            print("latitude:",self.coordinates[1])
            t2 = time.time()
            print("time taken to read = ","%g"%(t2-t1))


    def read_ROTI_ion(self,infile):
        self.nr_ROTI_ion_sets +=1
        self.unit =infile.readline().split()[0]
        for line in infile:
            line = line.split()
            if len(line)==0: #ignoring empty lines
                continue
            # print(line)
            if line[0] == "<EndOfVariable>": #ending
                break

    def read_ROTI_Grid(self,infile):
        self.unit =infile.readline().split()[0]
        counter = 0
        for line in infile:
            line = line.split()
            if len(line)==0: #ignoring empty lines
                continue
            if line[0] == "<EndOfVariable>": #ending
                self.nr_ROTI_grid_sets += 1
                break
            for i in range(len(line)):
                if line[i]=="9999999999":
                    line[i]=float("nan")
                self.data_grid_scint[i,counter,self.nr_ROTI_grid_sets]=float(line[i])
            counter+=1
    def read_comments(self,infile):
        nr_comments_read = 0
        for line in infile:
            line = line.split()
            if len(line)==0: #ignoring empty lines
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

    def read_grid(self,infile):
        begin_read = 0
        for line in infile:
            line = line.split()
            if line[0] == "<EndOfDefineGrid>": #ending
                begin_read = 0
            if begin_read:
                self.longitude=[float(line[0]),float(line[1]),float(line[2])]
                second_line = infile.readline().split()
                self.latitude = [float(second_line[0]),float(second_line[1]),\
                                     float(second_line[2])]
            if line[0] == '<StartOfDefineGrid>': #starting to read the grid
                begin_read = 1
            if line[0] == "<EndOfHeader>": #ending the read of the grid
                break


    def create_grid(self):
        if not len(self.longitude) or not len(self.latitude):
            raise SyntaxError("need to read the data first, using read_textfile")
        self.longitude_axis_size = int(abs(self.longitude[1] - self.longitude[0])\
                                    /self.longitude[2])+1
        self.latitude_axis_size = int(abs(self.latitude[1]- self.latitude[0])\
                                    /self.latitude[2]) +1

        self.data_grid_ion = -1*np.ones((self.longitude_axis_size,\
                                         self.latitude_axis_size,\
                                         30),dtype=float)
        self.data_grid_scint = -1*np.ones_like(self.data_grid_ion)



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

    @property
    def day_year(self):
        """
        returns of the day and year
        """
        self.check_read_data()
        return self.day, self.year



    def display_date(self):
        """
        displays the year and which day of the year
        """
        self.check_read_data()
        print("year: ",self.year," day: ", self.day)

    @property
    def ROTI_Grid_data(self):
        self.check_read_data()
        return self.data_grid_scint[:,:,0:self.nr_ROTI_grid_sets]

    @property
    def coordinates(self):
        return self.longitude, self.latitude

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    obj = ReadROTIData()
    obj.read_textfile("example_textfile_ROTI.txt")
    print("time",obj.time)
    print("latitude,longitude", obj.coordinates)
    data = obj.ROTI_Grid_data
    plt.imshow(data[:,:,0])
    plt.colorbar()
    plt.show()
    plt.imshow(data[:,:,1])
    plt.colorbar()
    plt.show()
