import numpy as np
import matplotlib.pyplot as plt

class ReadData():
    def __init__(self):
        """
        initializing variables and lists
        """
        #info about the file
        self.textfile = False # name for the textfile
        self.version_number = "No textdocument has been read"  #version of the file format
        self.version = -1
        self.receiver = "not read"
        #lists of info
        self._epochs = [] #list of times the data was taken
        self._data = [] # nested list of all the data unfiltered
        self._datasizes = []
        self._epochs_indexing = [] #list of the indexing
        self.satelittesystem = [] # list of the sattellite systems
        self.satelliteId = [] #list of satelitteId found in chronological
        self.data_dict = {} #dictionary to be filled with all the data
        #counters
        self.nr_satID = 0
        self.nr_satSys = 0
        self.nr_datapoints = 0
        self.nr_datasets = 0

    def read_textfile(self,textfile):
        """
        read textfile specified and selects the right textfile_reader based on
        what version the texfile is
        """
        # print("satelitteId longitude latitude elevation  S4_L1 SigmaPhi_L1 [] S4_L2 SigmaPhi_L2 []")
        self.textfile = textfile
        with open(textfile+".txt", 'r') as infile:
            self.version = infile.readline()[2:]
            self.version_number = float(self.version.split(" ")[1])
            self.receiver = infile.readline()[2:]
            if self.version_number == 1.3:
                self.read_version_1_3(infile)
            elif self.version_number == 1.1:
                self.read_version_1_1(infile)
            else:
                print("version_number = ",self.version_number)
                raise SyntaxError("version number not correct for this reader."\
                                 +"Only 1.1 and 1.3 used by this reader")

        self._create_indexes()
        #return table_array
        # return self.x


    def read_version_1_3(self, infile):
        """
        reads version 1.3 and sorts the information stored in the textfiles to
        the class variables
        """

        for line in infile:
            if not line[0] == "%" and not line[0] == "#":
                numbers = line.split(" ")
                if len(numbers) == 7:
                    #reads the epochs
                    self._epochs.append([int(float(i)) for i in numbers])
                    self._datasizes.append(int(float(numbers[-1])))
                    self.nr_datasets += 1

                elif len(numbers) > 7:
                    #read the data points
                    if sum([float(numbers[1])==i for i in self.satelliteId])==0:
                        self.satelliteId.append(numbers[1]) #taking satelitte number
                        self.nr_satID += 1
                    if sum([float(numbers[0])==i for i in self.satelittesystem])==0:
                        self.satelittesystem.append(numbers[1]) #taking satelitte number
                        self.nr_satID += 1

                    self._data.append(numbers)
                    self.nr_datapoints += 1
                else:
                    #checks if a line is too short (numbers <7)
                    raise ValueError("non-readable data in the textfile \n"\
                    +line + "data line to short to be read")

    def read_version_1_1(self,infile):
        for line in infile:
            if not line[0] == "%" and not line[0] == "#":
                numbers = line.split(" ")
                if len(numbers) == 7:
                    if float(numbers[0]) > 40:
                        #reads the epochs
                        self._epochs.append([int(float(i)) for i in numbers])
                        self._datasizes.append(int(float(numbers[-1])))
                        self.nr_datasets += 1

                    elif float(numbers[0]) < 40:
                        #reads the data points
                        if sum([float(numbers[0])==i for i in self.satelliteId])==0:
                            self.satelliteId.append(numbers[1]) #taking satelitte number
                            self.nr_satID += 1
                        self._data.append(numbers)
                        self.nr_datapoints += 1
                else:
                    #checks if a line is too short
                    raise ValueError("non-readable data in the textfile \n"\
                    +line + "data line to short to be read")



    def _create_indexes(self,):
        temp = -1
        for i in self._datasizes:
            temp += i
            self._epochs_indexing.append(temp)

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
        return np.array(self._datasizes[0:self.nr_datasets])


    @property
    def epochs(self):
        """
        returns the list of the times the data was retrived
        """
        self.check_read_data()
        return np.array(self._epochs[:])

    @property
    def satellite_Id(self):
        """
        return the satelitteId that the measurement used.
        """
        self.check_read_data()
        return np.array(self.satelliteId[0:self.nr_satID])


    @property
    def textdocument_version(self):
        """
        returns the version number of the file
        """
        self.check_read_data()
        return self.version_number

    #functions that display the data with print
    def textdocument_version_display(self):
        self.check_read_data()
        print(self.version)

    def receiver_display(self):
        self.check_read_data()
        print(self.receiver)

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

    def display_single_datapoint(self, index):
        """
        displays a single datpoint. (not functional yet)
        """
        self.check_read_data()
        print("unfinished function")


if __name__ == '__main__':
    obj = ReadData()
    obj.read_textfile("data/example_data_ver_1_3")
    print("datapoints = ",obj.datapoints)
    print(obj.datasizes)
    print(obj.epochs)
    #print(obj.epochs)
    #print(obj._epochs_indexing)
    # print(obj.textdocument_version)
    obj.textdocument_version_display()
