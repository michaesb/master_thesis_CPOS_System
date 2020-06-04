import numpy as np
import time,sys
sys.path.insert(1, "../") # to get access to adjecent packages in the repository
from extra.progressbar import progress_bar



class ReadRTIMData():
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
        self._epochs = [] #list of times the data was taken
        self._data = [] # nested list of all the data unfiltered
        self._datasizes = [] #the sizes of each epoch
        self._epochs_indexing = [] #list of the indexing
        self.satelittesystem = [] # list of the sattellite systems
        self._satelliteId = [] #list of satelitteId found in chronological
        self.data_dict = {} #dictionary to be filled with all the data (not in use)
        #Location of stations
        self._location = [] #location for display
        self._latitude = [] #latitude coordinate
        self._longitude = [] #longitude coordinate
        self._elevation = [] #elevation coordinate
        # for version 1.1
        #time
        self.start_time = [] # hour minute second
        self.end_time =  [] # hour minute second
        #L1 measurements
        self._S4_L1 = []
        self._sigma_phi_L1 =[]
        #L2 measurements
        self._S4_L2 = []
        self._sigma_phi_L2 =[]
        # version 1.3
        self._types_of_measurements = []
        self.C = [] #1C
        self.WW = [] #2W
        self.LL = [] #2L
        self.W = [] #1W
        self.QQQQQ = [] #5Q
        self.CC = [] #2C
        self.QQQQQQQ = [] #7Q
        self.QQQQQQQQ = [] #8Q
        self.CCCCCC = [] #6C
        # testing version 1.3
        self._list_of_scintillation_types = []
        #counters
        self.nr_satID = 0 #number of different satelitte used in the textfile
        self.nr_satSys = 0 #tracks the number of satelittesystem used in the texfile
        self.nr_datapoints = 0 # tracks the number of datapoints in the textfile
        self.nr_datasets = 0 # tracks the number of datasets

    def read_textfile(self,textfile, verbose=False, filter=False):
        """
        read textfile specified and selects the
        right textfile_reader based on what version the texfile is. Also reads
        the specifications for the for the data recording.
        """
        self.verbose = verbose
        self.filter = filter
        self.nr_lines = sum(1 for line in open(textfile)) #getting the number of lines
        self.textfile = textfile
        with open(textfile, 'r') as infile:
            #getting the version of the textfile
            self.version = infile.readline()[2:]
            self.version_number = float(self.version.split(" ")[3])
            # get the receiver name for the recorder
            self.receiver = infile.readline().split(" ")[2]
            # get the agency where the information was recorded by
            self.agency = infile.readline()[2:]
            # getting the date where the info is recorded
            date = infile.readline().split(" ")[2:]
            self.year, self.day_of_year = int(float(date[0])),int(float(date[1]))
            if self.version_number == 1.3:
                self.read_version_1_3(infile)
            elif self.version_number == 1.1:
                self.read_version_1_1(infile)
            else:
                raise SyntaxError("version number not correct for this reader."\
                                 +"Only 1.1 and 1.3 used by this reader")
        self._create_indexes()
        self._check_data_extraction()

    #reads the different versions of the textfiles
    def read_version_1_3(self,infile3):
        """
        reads version 1.3 and sorts the information stored in the textfiles to
        the class variables
        """
        if self.verbose:
            count = 0
            print("reading a version 1.3 with "+ str(self.nr_lines) +" lines")
            t0 = time.time()
        for line in infile3:
            if not line[0] == "%" and not line[0] == "#":
                #removing empty spaces from the list
                raw_numbers = line.split(" ")
                numbers = []
                for i in raw_numbers:
                    if not i == "":
                        numbers.append(i)

                if self.verbose:
                    count +=1
                    progress_bar(count,self.nr_lines)

                if len(numbers) == 7:
                    #reads the epochs
                    self._epochs.append([int(float(i)) for i in numbers])

                    self._datasizes.append(int(float(numbers[-1])))
                    self.nr_datasets += 1

                elif len(numbers) > 7:
                    #read the data points
                    if sum([float(numbers[0])==i for i in self.satelittesystem])==0:
                        self.satelittesystem.append(int(float(numbers[0]))) #taking satelitte number
                        self.nr_satSys += 1
                    if sum([float(numbers[1])==i for i in self._satelliteId])==0:
                        self._satelliteId.append(int(float(numbers[1]))) #taking satelitte number
                        self.nr_satID += 1
                    nr_measurements = (len(numbers)-7)/4 #measurements after 7 every 4
                    # print("numbers",len(numbers), "measurements", nr_measurements)

                    for i in range(int(nr_measurements)):
                        if sum([numbers[7+4*i]==j for j in self._types_of_measurements])==0:
                            self._types_of_measurements.append(numbers[7+4*i])
                    # self._data.append(numbers)
                    self.nr_datapoints += 1
                else:
                    #checks if a line is too short (numbers <7)
                    raise ValueError("non-readable data in the textfile \n"\
                    +line + "data line to short to be read")
        if self.verbose:
            t2 =time.time()
            print("time taken to read = ","%g"%(t2-t1) )
        print(self._types_of_measurements)

    def read_version_1_1(self,infile1):
        """
        reads version 1.1 and sorts the information stored in the textfiles to
        the class variables
        """
        if self.verbose:
            count = 0
            print("reading version 1.1 with "+ str(self.nr_lines) +" lines")
            t1 = time.time()
        time_counter=0
        for line in infile1:
            if not line[0] == "%" and not line[0] == "#":
                raw_numbers = line.split(" ")
                numbers = []
                for i in raw_numbers:
                    if not i == "":
                        numbers.append(i)
                if self.verbose:
                    count +=1
                    progress_bar(count,self.nr_lines)

                if int(float(numbers[0])) > 1900: #checking for year
                    #reads the epochs
                    if self.nr_datasets == 0:
                        self.start_time = [float(numbers[3]), float(numbers[4])]
                    self.end_time = [float(numbers[3]), float(numbers[4])]
                    self._datasizes.append(int(float(numbers[-1])))
                    self.nr_datasets += 1
                elif int(float(numbers[0])) < 62: #checking if satelitteId
                    #reads the data points
                    # print("praise Cthulu, destroyer of worlds")
                    # self._data.append(numbers) #saving data for debugging purposes
                    # satelitteId

                    if self.filter:
                        if float(numbers[4])>2 or float(numbers[5])>2*np.pi:
                            continue
                        if float(numbers[7])>2 or float(numbers[8])>2*np.pi:
                            continue
                    if sum([float(numbers[0])==i for i in self._satelliteId])==0:
                        self._satelliteId.append(int(float(numbers[0]))) #taking satelitte number
                        self.nr_satID += 1
                    #Location
                    if sum([float(numbers[1])==i for i in self._longitude])==0:
                        self._location.append([float(numbers[1]),float(numbers[2]),\
                                               float(numbers[3])])
                    #locations
                    self._longitude.append(float(numbers[1]))
                    self._latitude.append(float(numbers[2]))
                    self._elevation.append(float(numbers[3]))
                    #L1
                    self._S4_L1.append(float(numbers[4]))
                    self._sigma_phi_L1.append(float(numbers[5]))
                    #L2
                    self._S4_L2.append(float(numbers[7]))
                    self._sigma_phi_L2.append(float(numbers[8]))
                    if float(numbers[8])>1e+5:
                        print(numbers)
                    #counting datapoints
                    self.nr_datapoints += 1 #counting the datapoints
                else:

                    raise ValueError("non-readable data in the textfile \n"\
                    +line+ str(len(numbers)) + "data line to short to be read")
                    # + line+ str(self.nr_datapoints)) #for debugging purposes
        if self.verbose:
            t2 =time.time()
            print("time taken to read = ","%g"%(t2-t1))
    #different checks and internal programs that other functions use
    def _create_indexes(self):
        """
        creates indexes to retrieve information from :::: (Unfinished)
        """
        temp = -1
        self._epochs_indexing.append(0)
        for i in self._datasizes:
            temp += i
            self._epochs_indexing.append(temp)
        self._epochs_indexing.append(-1)


    def _check_data_extraction(self):
        """
        Internal tests to check that reading the textfile correctly
        """
        #checks that the number of read datapoints, matches the specified sizes
        #of the datasets
        if not np.sum(self._datasizes) == self.nr_datapoints:
            print("Warning: number of datapoints, not equal to all datasizes"\
                   +"might still work, but something may be incorrect")

    def check_read_data(self):
        """
        A test for the funtions that returns data.
        This raises an error and exits, if the read_data function
        has not been used.
        """
        if not self.textfile:
            raise SyntaxError("need to read the data first, using read_textfile")
            exit()

    def check_measurements_type(self):
        """
        A test for version 1.3, where we check the measurement types with the
        known test types, so the user can receive a warning that unfamiliar types
        are being read and therefore ignored.
        """
        common_types = ["1C", "2W", "2L", "1W", "5Q", "2C", "7Q", "8Q", "6C"]
        if sum([common_types==i for i in self._types_of_measurements])==0:
            pass



    # properties that return information about the dataset

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


    def time(self, unit=0,start_time=0):
        """
        returns the time from the start of the data and to the end data
        This assumes that it's continous and gives multiple output based on the
        parameter unit. unit=0 gives seconds, unit =1 gives minutes, unit = 2
        gives hours.
        """
        self.check_read_data()
        hours = self.end_time[0]-self.start_time[0]
        minutes = self.end_time[1]-self.start_time[1]

        if unit ==0:
            duration = minutes+ hours*60
        if unit ==1:
            duration = minutes/60 + hours
        n = len(self._S4_L1)
        t = np.linspace(0,duration,n)
        return t

    @property
    def satellite_Id(self,):
        """
        return the satelitteId that the measurement used.
        """
        self.check_read_data()
        return np.sort(np.array(self._satelliteId))

    @property
    def L1_data(self):
        """
        Returns the S4 measurements L1 and L2.
        """
        self.check_read_data()
        return np.array(self._S4_L1),np.array(self._sigma_phi_L1)

    @property
    def L2_data(self):
        """
        Returns the sigma measurements L1 and L2.
        """
        self.check_read_data()
        return np.array(self._S4_L2),np.array(self._sigma_phi_L2)

    @property
    def textdocument_version(self):
        """
        returns the version number of the file
        """
        self.check_read_data()
        return self.version_number

    @property
    def day_year(self):
        """
        returns of the day and year
        """
        self.check_read_data()
        return self.day_of_year, self.year

    @property
    def location(self,):
        """
        returns the locations of the measurements (non repatative)
        """
        self.check_read_data()
        return np.array(self._location)

    #functions that display the data with print

    def display_date(self):
        """
        displays the year and which day of the year
        """
        self.check_read_data()
        print("year: ",self.year," day: ", self.day_of_year )

    def textdocument_version_display(self):
        """
        displays the version of the textfile
        """
        self.check_read_data()
        print(self.version)

    def receiver_display(self):
        """
        displays which kind of receiver is used in the textfile
        """
        self.check_read_data()
        print("Receiver: "+self.receiver)

    def display_epochs(self):
        """
        Prints the times the data was retrived in a table
        """
        self.check_read_data()
        print("--------------------------------")
        print ("year", " month","day", "hour", "minute", "second", "nrofDataRecords","\n")
        for i in range(len(self._epochs)):
            for j in range(len(self._epochs[i])):
                print(self._epochs[i][j], end="     ")
            print("\n")
        print("--------------------------------")

    def display_data(self):
        """
        Display the data in a table form. (needs develepment to make the data.
        readable)
        """
        self.check_read_data()
        if self.version_number == 1.3:
            print("not working for 1.3")
            # print("--------------------------------")
            # for i in range(len(self._data)):
            #     print("_satelliteId", "longitude", "latitude", "elevation", "S4_L1",\
            #     "SigmaPhi_L1", "[RESERVED/NOTINUSE]", "S4_L2", "SigmaPhi_L2", "[RESERVED/NOTINUSE]")
            #     for j in range(len(self._data[i])):
            #         print(self._data[i][j], end=" ")
            #     print("\n")
            # print("--------------------------------")
        if self.version_number == 1.1:
            print("--------------------------------")
            for i in range(len(self._data)):
                print("_satelliteId", "longitude", "latitude", "elevation", "S4_L1",\
                "SigmaPhi_L1", "slope L1", "S4_L2", "SigmaPhi_L2", "L2_slope")
                for j in range(len(self._data[i])):
                    print(self._data[i][j], end=" ")
                print("\n")
            print("--------------------------------")

    def display_location_satellite(self):
        """
        only works for version 1.3
        """
        self.check_read_data()
        print("--------------------------------")
        print("_satelliteId", "longitude", "latitude")
        for i in range(len(self._data)):
            for j in range(3):
                print(self._data[i][j], end="          |")
            print("\n")
        print("--------------------------------")

    def display_single_datapoint(self, index):
        """
        displays a single datpoint. (not functional yet)
        self.check_read_data()
        """
        print("not functional yet")


if __name__ == '__main__':


    obj1_1 = ReadRTIMData()
    obj1_1.read_textfile("example_data_ver_1_1.txt")
    obj1_1.receiver_display()
    print(obj1_1.time(unit=0), len(obj1_1.time(unit=0)))
    # obj1_3 = ReadData()
    # obj1_3.read_textfile("example_data_ver_1_3.txt")
    # obj1_3.receiver_display()
    #
