import numpy as np
import time, sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar
import matplotlib.pyplot as plt
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
        self.month = -1 #which month the data is recorded
        self.day = -1  #which day the data is recorded

        #time
        self.start_time = [] # hour, minute, second
        self.end_time =  [] # hour, minute, second
        #data
        self.nr_datapoints = 0
        #position data
        self.north_pos = False
        self.south_pos = False
        self.east_pos = False
        self.west_pos = False
        #
        self.quality_indicator_explained= ["0: Fix not available or invalid",
                                            "1: GPS SPS Mode, fix valid",
                                            "2:Differential GPS SPS Mode, fix valid",
                                            "3: GPS PPS Mode, fix valid",
                                            "4:RTK Fix solution",
                                            "5:RTK Float solution",
                                            "6:Estimated (dead reckoning) mode",
                                            "7:Manual input mode",
                                            "8:Simulator mode"]
        self.quality_indicator_types = []
        self.nr_satellite = -1
        self.HDOP = -1
        self.HDOP_unit = -1
        self.geo_seperation = -1
        self.geo_seperation_unit = -1
        self.age_of_data = -1

    def read_textfile(self,textfile, verbose=False):
        """
        read textfile specified and selects the
        right textfile_reader based on what version the texfile is. Also reads
        the specifications for the for the data recording.
        """
        self.verbose = verbose
        self.nr_datapoints = sum(1 for line in open(textfile)) #getting the number of lines
        self.textfile = textfile
        if self.verbose:
            print("reading NMEA textfile with " +str(self.nr_datapoints)+" lines")
            t1 = time.time()
        count_line = 0
        #creating arrays when you have the number of points
        self.initilize_arrays()
        #opening the textfile
        with open(textfile, 'r') as infile:
            for line in infile:
                #extractin the infor in 3 parts, the date, time and position data
                self.date, time_temp, data_line = line.split()
                #splitting the the data into multiple parts based on the comma
                data_line = data_line.split(",")
                #Grabbing initial data from line
                if count_line ==0:
                    self.start_time = float(time_temp[0:1]),\
                                      float(time_temp[3:4]),\
                                      float(time_temp[6:7])
                    self._talker_identifier = data_line[0] #setting the type of identifier
                    #Seing which coordinate is being displayed
                    if data_line[3] == "N":
                        self.north_pos =True
                    if data_line[3] == "S":
                        self.south_pos =True
                    if data_line[5] == "E":
                        self.east_pos =True
                    if data_line[5] == "W":
                        self.west_pos =True
                    self.HDOP_unit = data_line[10]
                    self.geo_seperation_unit = data_line[12]

                if self._talker_identifier != data_line[0]:
                    print("different talker_identifier",data_line[0],"not",\
                           self._talker_identifier)

                #filling position arrays
                if self.north_pos:
                    self.north_position[count_line] = float(data_line[2])
                if self.south_pos:
                    self.south_position[count_line] = float(data_line[2])
                if self.east_pos:
                    self.east_position[count_line] = float(data_line[4])
                if self.west_pos:
                    self.west_position[count_line] = float(data_line[4])
                #quality indicator
                if sum([int(data_line[6])==i for i in self.quality_indicator_types])==0:
                    self.quality_indicator_types.append(int(data_line[6]))
                self.quality_indicator[count_line] = data_line[6]
                #number of satellites
                self.nr_satellite[count_line] = data_line[7]
                # Horizontal dilution of precision
                self.HDOP[count_line] = data_line[8]
                # measurements of height in the point
                self.altitude[count_line]= data_line[9]
                # geoidal seperation
                self.geo_seperation[count_line] = data_line[11]
                # age of differential GPS data
                if data_line[13]=="":
                    self.age_of_data[count_line] = float("nan")
                else:
                    self.age_of_data[count_line] = data_line[13]

                # self.something[count_line]= data_line[14]
                #keeping a counter of the lines in the textfile document
                count_line+=1

        print(len(data_line))

        self.end_time = float(time_temp[0:2]),\
                        float(time_temp[3:5]),\
                        float(time_temp[6:8])


        if self.verbose:
            t2 = time.time()
            print("time taken to read = %g"%(t2-t1))

    #intiliziing arrays and tests
    def check_read_data(self):
        """
        A test for the funtions that returns data.
        This raises an error and exits, if the read_data function
        has not been used.
        """
        if not self.textfile:
            raise SyntaxError("need to read the data first, using read_textfile")
            exit()

    def initilize_arrays(self,):
        #postion arrays
        self.north_position = np.zeros(self.nr_datapoints, dtype =float)
        self.east_position = np.zeros(self.nr_datapoints, dtype =float)
        self.west_position = np.zeros(self.nr_datapoints, dtype =float)
        self.south_position = np.zeros(self.nr_datapoints, dtype =float)
        self.quality_indicator = np.zeros(self.nr_datapoints, dtype=int)
        self.nr_satellite = np.zeros(self.nr_datapoints, dtype=int)
        self.HDOP = np.zeros(self.nr_datapoints,dtype = float)
        self.altitude = np.zeros(self.nr_datapoints,dtype = float)
        self.geo_seperation= np.zeros(self.nr_datapoints,dtype=float)
        self.age_of_data = np.zeros(self.nr_datapoints,dtype=float)
        # self.something = np.zeros(self.nr_datapoints, dtype=)
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
        duration = np.ceil(minutes+ hours*60. +seconds/60.)
        t = np.linspace(self.start_time[1],self.start_time[1]+duration,\
                        int(self.nr_datapoints/60.)+1)
        return t

    @property
    def time_h(self):
        """
        returns the time from the start of the data and to the end data
        This assumes that it's continous and there are 5 minutes in between the
        points
        """
        self.check_read_data()
        hours = self.end_time[0]-self.start_time[0]
        minutes = self.end_time[1]-self.start_time[1]
        seconds = self.end_time[2]-self.start_time[2]
        duration = np.ceil(hours+ minutes/60. +seconds/3600.)
        t = np.linspace(self.start_time[1],self.start_time[1]+duration,\
                        self.nr_datapoints)
        print(t)
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

    @property
    def talker_identifier(self,):
        """
        returns the type of talker identifier
        """
        self.check_read_data()
        return self._talker_identifier

    @property
    def coordinates(self):
        """
        returns the coordinates in the data. to be worked on
        """
        self.check_read_data()
        return self.north_position, self.east_position, self.altitude

    @property
    def qualities_indicator(self):
        """
        returns an array of all the indicators to the data
        """
        self.check_read_data()
        return self.qualities_indicator

    @property
    def nr_satellites(self):
        """
        returns an array of all nr of satellites in the data
        """
        self.check_read_data()
        return self.nr_satellite

    @property
    def horizontal_dil_of_pos(self):
        """
        returns an array of all nr of satellites in the data
        """
        self.check_read_data()
        return self.HDOP

    @property
    def geoidal_seperation(self):
        """
        returns the difference between the earths ellipsoid and geoid
        """
        self.check_read_data()
        return self.geo_seperation


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

    def display_coordinates_type(self,):
        """
        Display the type of coordinates taken from the data
        """
        self.check_read_data()
        axis= ""
        if self.north_pos:
            axis = axis+ "North and "
        if self.south_pos:
            axis = axis + "South and "
        if self.east_pos:
            axis = axis +"East"
        if self.west_pos:
            axis = axis + "West"
        axis = axis + " coordinates"
        print(axis)

    def display_coordinates(self):
        """
        display the positions arrays
        """
        self.check_read_data()
        for i in range(self.nr_datapoints):
            if self.north_pos:
                print("N",self.north_position[i], end = " ")
            if self.south_pos:
                print("S",self.south_position[i], end = " ")
            if self.east_pos:
                print(" E",self.east_position[i])
            if self.west_pos:
                print(" W",self.west_position[i])

    def display_GPS_indicator(self):
        """
        displaying the quaility of the data.
        """
        self.check_read_data()
        for i in self.quality_indicator_types:
            ratio = 100*np.sum(i==j for j in self.quality_indicator)/self.nr_datapoints
            print(self.quality_indicator_explained[i], round(ratio,2))

if __name__ == '__main__':
    obj = ReadNMEAData()
    obj.read_textfile("example_textfile_NMEA.txt", verbose=True)
    print(obj.datapoints,"nr_datapoints")
    print(obj.talker_identifier)
    print(obj.day_year, "day_year")
    print(obj.time_period, "time")
    print(obj.quality_indicator, "indicator")
    print(obj.nr_satellite,"sat")
    print(obj.horizontal_dil_of_pos, "dil of pos")
    print(obj.geoidal_seperation, "geoid and ellipse")
    #obj.display_GPS_indicator()
    N, E, Z = obj.coordinates
    plt.plot(N)
    plt.title(str(N[0]))
    plt.show()
    plt.plot(E)
    plt.title(str(E[0]))
    plt.show()
    plt.plot(Z)
    plt.title(str(Z[0]))
    plt.show()
    # obj.display_coordinates_type()
    # obj.display_coordinates()
