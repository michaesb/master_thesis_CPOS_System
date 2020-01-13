import numpy as np
import matplotlib.pyplot as plt

class ReadData():
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
        #lists of info
        self._epochs = [] #list of times the data was taken
        self._data = [] # nested list of all the data unfiltered
        self._datasizes = [] #the sizes of each epoch
        self._epochs_indexing = [] #list of the indexing
        self.satelittesystem = [] # list of the sattellite systems
        self.satelliteId = [] #list of satelitteId found in chronological
        self.data_dict = {} #dictionary to be filled with all the data (not in use)
        #L1 measurements
        self._S4_L1 = []
        self._sigma_phi_L1 =[]
        self._slope_L1 = []
        #L2 measurements
        self._S4_L2 = []
        self._sigma_phi_L2 =[]
        self._slope_L2 = []
        #counters
        self.nr_satID = 0 #number of different satelitte used in the textfile
        self.nr_satSys = 0 #tracks the number of satelittesystem used in the texfile
        self.nr_datapoints = 0 # tracks the number of datapoints in the textfile
        self.nr_datasets = 0 # tracks the number of datasets

    def read_textfile(self,textfile):
        """
        read textfile (without .txt at teh end) specified and selects the
        right textfile_reader based on what version the texfile is. Also reads
        the specifications for the for the data recording.
        """
        # print("satelitteId longitude latitude elevation  S4_L1 SigmaPhi_L1 [] S4_L2 SigmaPhi_L2 []")
        self.textfile = textfile
        with open(textfile+".txt", 'r') as infile:
            #getting the version of the textfile
            self.version = infile.readline()[2:]
            self.version_number = float(self.version.split(" ")[1])
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

        for line in infile3:
            if not line[0] == "%" and not line[0] == "#":
                numbers = line.split(" ")
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
                    if sum([float(numbers[1])==i for i in self.satelliteId])==0:
                        self.satelliteId.append(int(float(numbers[1]))) #taking satelitte number
                        self.nr_satID += 1
                    self._data.append(numbers)
                    self.nr_datapoints += 1
                else:
                    #checks if a line is too short (numbers <7)
                    raise ValueError("non-readable data in the textfile \n"\
                    +line + "data line to short to be read")

    def read_version_1_1(self,infile1):
        """
        reads version 1.1 and sorts the information stored in the textfiles to
        the class variables
        """

        for line in infile1:
            if not line[0] == "%" and not line[0] == "#":
                numbers = line.split(" ")

                if int(float(numbers[0])) > 1900: #checking if year
                    #reads the epochs
                    self._epochs.append([int(float(i)) for i in numbers])
                    self._datasizes.append(int(float(numbers[-1])))
                    self.nr_datasets += 1


                elif int(float(numbers[0])) < 40: #checking if satelitteId
                    #reads the data points
                    self._data.append(numbers) #saving data for debugging purposes
                    # satelitteId
                    if sum([float(numbers[0])==i for i in self.satelliteId])==0:
                        self.satelliteId.append(int(float(numbers[0]))) #taking satelitte number
                        self.nr_satID += 1
                    #Location


                    #L1
                    self._S4_L1.append(int(float(numbers[4])))
                    self._sigma_phi_L1.append(int(float(numbers[5])))
                    self._slope_L1.append(int(float(numbers[6])))
                    #L2
                    self._S4_L2.append(int(float(numbers[7])))
                    self._sigma_phi_L2.append(int(float(numbers[8])))
                    self._slope_L2.append(int(float(numbers[9])))

                    self.nr_datapoints += 1 #counting the datapoints
                else:

                    raise ValueError("non-readable data in the textfile \n"\
                    +line + "data line to short to be read")
                    # + line+ str(self.nr_datapoints)) #for debugging purposes

    #different checks and internal programs that other functions use
    def _create_indexes(self):
        """
        creates indexes to retrieve information from :::: (Unfinished)
        """
        temp = -1
        for i in self._datasizes:
            temp += i
            self._epochs_indexing.append(temp)

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

    # properties that return lengths and information about the dataset

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
    def satellite_Id(self,):
        """
        return the satelitteId that the measurement used.
        """
        self.check_read_data()
        return np.sort(np.array(self.satelliteId))


    @property
    def S4(self):
        """
        Returns the S4 measurements L1 and L2.
        """
        self.check_read_data()
        return np.array(self._S4_L1),np.array(self._S4_L2)

    @property
    def Sigma(self):
        """
        Returns the sigma measurements L1 and L2.
        """
        self.check_read_data()
        return np.array(self._sigma_phi_L1),np.array(self._sigma_phi_L2)


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

    #functions that display the data with print
    def display_date(self):
        """
        displays the year and which day of the year
        """
        self.check_read_data()
        print("year: ",self.year," date: ", self.day_of_year )

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
        print("--------------------------------")
        for i in range(len(self._data)):
            print("satelliteId", "longitude", "latitude", "elevation", "S4_L1",\
            "SigmaPhi_L1", "[RESERVED/NOTINUSE]", "S4_L2", "SigmaPhi_L2", "[RESERVED/NOTINUSE]")
            for j in range(len(self._data[i])):
                print(self._data[i][j], end=" ")
            print("\n")
        print("--------------------------------")

    def display_location_satellite(self):
        self.check_read_data()
        print("--------------------------------")
        print("satelliteId", "longitude", "latitude")
        for i in range(len(self._data)):
            for j in range(3):
                print(self._data[i][j], end="          |")
            print("\n")
        print("--------------------------------")

    #plotting functions that let you visualise the data
    #and view simple parts of it

    def plotting_disturbances(self):
        """
        plotting all disturbances. Not functionning yet.
        """
        self.check_read_data()
        plt.plot()
        plt.xlabel("time")
        plt.ylabel("S4")
        plt.title("")
        plt.show()
        print("not functional yet")

    def display_single_datapoint(self, index):
        """
        displays a single datpoint. (not functional yet)
        self.check_read_data()
        """
        print("not functional yet")


if __name__ == '__main__':
    obj1_1 = ReadData()
    obj1_1.read_textfile("data/example_data_ver_1_1")
    obj1_1.receiver_display()

    obj1_3 = ReadData()
    obj1_3.read_textfile("data/example_data_ver_1_3")
    obj1_3.receiver_display()
