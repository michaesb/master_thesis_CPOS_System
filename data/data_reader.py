import numpy as np
import matplotlib.pyplot as plt

class ReadData():
    def __init__(self):
        """
        initializing variables and lists
        """
        self.textfile = False # name for the textfile
        self._epochs = [] #list of times the data was taken
        self._data = [] # nested list of all the data unfiltered
        self._datasizes = []
        self._epochs_indexing = [] #list of the indexing
        self.satelliteId = [] #list of satelitteId found in chronological
        self.data_dict = {}
        #counters
        self.nr_satID = 0
        self.nr_datapoints = 0
        self.nr_datasets = 0

    def read_textfile(self,textfile):
        """
        read textfile specified in the input and extract data from the data
        """
        print("satelitteId longitude latitude elevation  S4_L1 SigmaPhi_L1 [] S4_L2 SigmaPhi_L2 []")
        with open(textfile+".txt", 'r') as infile:
            self.textfile = textfile
            for line in infile:
                if not line[0] == "%" and not line[0] == "#":
                    numbers = line.split(" ")
                    # print(len(numbers))
                    if len(numbers) == 7:
                        self._epochs.append([int(float(i)) for i in numbers])
                        self._datasizes.append(int(float(numbers[-1])))
                        self.nr_datasets += 1

                    elif len(numbers) > 7:
                        if sum([float(numbers[0])==i for i in self.satelliteId])==0:
                            self.satelliteId.append(numbers[1]) #taking satelitte number
                            self.nr_satID += 1
                        # print(numbers[1:8],numbers[9],numbers[11:])
                        # self._data.append(numbers)
                        self.nr_datapoints += 1
                        # print ("Perfectly balanced as all thing should be")
                    else:
                        print (line, "data line to short to be read")
                        raise ValueError("non-readable data in the textfile")
        print(self._datasizes)
        self.create_indexes()
        #return table_array
        # return self.x

    def create_indexes(self,):
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
    def epochs(self):
        """
        returns the list of the times the data was retrived
        """
        self.check_read_data()
        return self._epochs

    @property
    def satellite_Id(self):
        """
        return the satelitteId that the measurement was used.

        """
        self.check_read_data()
        return np.array(self.satelliteId[0:self.nr_satID])

    #functions that display the data in table form

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
        displays a single datpoint
        """
        print()


if __name__ == '__main__':
    obj = ReadData()
    obj.read_textfile("data/example_data")
    # obj.display_epochs()
    obj.display_location_satellite()
    # print(obj.epochs)
    # print(obj._epochs_indexing)
