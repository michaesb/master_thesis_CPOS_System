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
        # quality indicator
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
        self.checksum = []
        self.nr_lines = -1

        #WGS-84 geodetic constants
        self.semi_major_a = 6378137.0  # WGS-84 Earth semimajor axis (m)
        self.semi_minor_b = 6356752.314245 # Derived Earth semiminor axis (m)
        self.flat = (self.semi_major_a - self.semi_minor_b) / self.semi_major_a; # Ellipsoid Flatness
        self.flat_inv = 1.0 / self.flat;  # Inverse flattening

        #self.flat_inv = 298.257223563 #WGS-84 Flattening Factor of the Earth
        #self.semi_minor_b = a - a / f_inv
        #self.flat = 1.0 / f_inv;

    def read_textfile(self, textfile, verbose=False, filter_4=True):
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
            if filter_4:
                print("filtering data that is not a fix position")
            t1 = time.time()
        count_line = 0
        #creating arrays when you have the number of points
        self.initilize_arrays()
        #opening the textfile
        with open(textfile, 'r') as infile:
            for line in infile:
                #extracting the info in 3 parts, the date, time and position data
                self.date, time_temp, data_line = line.split()
                #splitting the the data into multiple parts based on the comma
                data_line = data_line.split(",")
                #Grabbing initial data from line
                if sum([int(data_line[6])==i for i in self.quality_indicator_types])==0:
                    self.quality_indicator_types.append(int(data_line[6]))

                self.quality_indicator[count_line] = data_line[6]

                if count_line ==0:
                    self.start_time = float(time_temp[0:1]),\
                                      float(time_temp[3:4]),\
                                      float(time_temp[6:7])
                    #setting the type of identifier
                    self._talker_identifier = data_line[0]

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
                    #

                #checking if the talker changes as one reads the file
                if self._talker_identifier != data_line[0]:
                    print("different talker_identifier",data_line[0],"not",\
                           self._talker_identifier)

                if float(data_line[6]) == 4 or not filter_4:
                    # print(count_line, data_line)
                    #filling position arrays
                    degrees_lat, arcminutes_lat = float(data_line[2][:2]), float(data_line[2][2:])
                    degrees_long, arcminutes_long = float(data_line[4][:3]), float(data_line[4][3:])
                    if self.north_pos:
                        self.north_position_temp[self.nr_datapoints] = degrees_lat + arcminutes_lat/60
                    if self.south_pos:
                        self.south_position_temp[self.nr_datapoints] = degrees_lat + arcminutes_lat/60
                    if self.east_pos:
                        self.east_position_temp[self.nr_datapoints] = degrees_long + arcminutes_long/60
                    if self.west_pos:
                        self.west_position_temp[self.nr_datapoints] = degrees_long + arcminutes_long/60
                    #number of satellites
                    self.nr_satellite_temp[self.nr_datapoints] = data_line[7]

                    # Horizontal dilution of precision
                    self.HDOP_temp[self.nr_datapoints] = data_line[8]

                    # measurements of height in the point
                    self.altitude_temp[self.nr_datapoints]= data_line[9]

                    # geoidal seperation
                    self.geo_seperation_temp[self.nr_datapoints] = data_line[11]

                    # age of differential GPS data
                    if data_line[13]=="":
                        self.age_of_data_temp[self.nr_datapoints] = float("nan")
                    else:
                        self.age_of_data_temp[self.nr_datapoints] = data_line[13]

                    #getting station_ID and checksum
                    diff_station_ID,checksum = data_line[14].split("*")

                    if diff_station_ID == "":
                        self.diff_station_ID_temp[self.nr_datapoints] = float("nan")
                    else:
                        self.diff_station_ID_temp[self.nr_datapoints] = diff_station_ID
                    self.checksum.append(checksum)
                    self.nr_datapoints+=1
                #keeping a counter of the lines in the textfile document
                count_line+=1
        # end of for loop
        self.shorten_arrays() #Shorten the arrays so if you filter the data,
                              #they are the correct size in the output.
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

    def initilize_arrays(self):
        """
        initialize the arrays as the number of points is established
        """
        #postion arrays
        self.north_position_temp = np.zeros(self.nr_lines, dtype =float)
        self.east_position_temp = np.zeros(self.nr_lines, dtype =float)
        self.west_position_temp  = np.zeros(self.nr_lines, dtype =float)
        self.south_position_temp = np.zeros(self.nr_lines, dtype =float)
        self.altitude_temp  = np.zeros(self.nr_lines,dtype = float)
        self.HDOP_temp = np.zeros(self.nr_lines,dtype = float)

        self.quality_indicator = np.zeros(self.nr_lines, dtype=int)
        self.nr_satellite_temp = np.zeros(self.nr_lines, dtype=int)

        self.geo_seperation_temp = np.zeros(self.nr_lines,dtype=float)
        self.age_of_data_temp = np.zeros(self.nr_lines,dtype=float)
        self.diff_station_ID_temp = np.zeros(self.nr_lines, dtype=float)

    def shorten_arrays(self):
        """
        shortening the arrays so they use less ram.
        """
        #creating shorter arrays
        self.north_position = np.zeros(self.nr_datapoints, dtype =float)
        self.east_position = np.zeros(self.nr_datapoints, dtype =float)
        self.west_position = np.zeros(self.nr_datapoints, dtype =float)
        self.south_position = np.zeros(self.nr_datapoints, dtype =float)
        self.altitude = np.zeros(self.nr_datapoints,dtype = float)
        self.HDOP = np.zeros(self.nr_datapoints,dtype = float)

        self.nr_satellite = np.zeros(self.nr_datapoints, dtype=int)

        self.geo_seperation= np.zeros(self.nr_datapoints,dtype=float)
        self.age_of_data = np.zeros(self.nr_datapoints,dtype=float)
        self.diff_station_ID = np.zeros(self.nr_datapoints, dtype=float)
        # Transfering the values to the shorter arrays
        self.north_position = self.north_position_temp[:self.nr_datapoints]
        self.east_position = self.east_position_temp [:self.nr_datapoints]
        self.west_position = self.west_position_temp[:self.nr_datapoints]
        self.south_position = self.south_position_temp[:self.nr_datapoints]
        self.altitude = self.altitude_temp[:self.nr_datapoints]
        self.HDOP = self.HDOP_temp[:self.nr_datapoints]

        self.nr_satellite = self.nr_satellite_temp[:self.nr_datapoints]

        self.geo_seperation = self.geo_seperation_temp[:self.nr_datapoints]
        self.age_of_data = self.age_of_data_temp[:self.nr_datapoints]
        self.diff_station_ID = self.diff_station_ID_temp[:self.nr_datapoints]

    #properties returns value
    @property
    def datapoints(self):
        """
        returns the number of datapoints extracted from the file.
        """
        self.check_read_data()
        if self.nr_datapoints != self.nr_lines:
            return self.nr_datapoints,self.nr_lines
        else:
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
    def talker_identifier(self):
        """
        returns the type of talker identifier
        """
        self.check_read_data()
        return self._talker_identifier

    @property
    def coordinates(self):
        """
        returns the coordinates in the data. with a transformation of axis.
        From degrees to meters.
        """
        self.check_read_data()
        e_sq = self.flat * (2 - self.flat)
        lambda_ = np.pi*self.north_position/180;
        phi = np.pi*self.east_position/180;
        s = np.sin(lambda_);
        N = self.semi_major_a / np.sqrt(1 - e_sq * s * s);
        north = (self.altitude + N) * np.cos(lambda_) * np.cos(phi);
        east = (self.altitude + N) * np.cos(lambda_) * np.sin(phi);
        altitude = (self.altitude + (1 - e_sq) * N) * np.sin(lambda_);
        return north, east, altitude

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

    @property
    def station_ID(self):
        """
        returns an array of the station ID
        """
        self.check_read_data()
        return self.diff_station_ID

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

    def display_coordinates_type(self):
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
        Not functional when filter is on
        """
        self.check_read_data()
        print("checking the quality of the data ------")
        for i in self.quality_indicator_types:
            ratio = 100*sum(i==j for j in self.quality_indicator)/self.nr_lines
            print(self.quality_indicator_explained[i], round(ratio,2), "%")
        print("---------------------------------------")

if __name__ == '__main__':
    obj = ReadNMEAData()
    obj.read_textfile("example_textfile_NMEA.txt", verbose=True)
    print(obj.datapoints,"nr_datapoints")
    print(obj.day_year, "day_year")
    print(obj.time_period, "time")
    print("time_m", obj.time_m)
    print(obj.quality_indicator, "indicator")
    print(obj.nr_satellite,"sat")
    print(obj.horizontal_dil_of_pos, "dil of pos")
    obj.display_GPS_indicator()
    N, E, Z = obj.coordinates
    ave_N, ave_E, ave_Z = np.sum(N)/obj.nr_datapoints,\
    np.sum(E)/obj.nr_datapoints ,np.sum(Z)/obj.nr_datapoints
    satellites = obj.nr_satellite
    plt.plot(N-ave_N)
    plt.title(str(N[0]))
    plt.show()
    plt.plot(E-ave_E)
    plt.title(str(E[0]))
    plt.show()
    plt.plot(Z-ave_Z)
    plt.title(str(Z[0]))
    plt.show()
    plt.plot(satellites)
    plt.title("satellites")
    plt.show()
