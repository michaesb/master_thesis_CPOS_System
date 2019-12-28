import numpy as np
import matplotlib.pyplot as plt

class ReadData():
    def __init__(self):
        """
        initializing variables
        """
        self.textfile = False
        self._epochs = [] #list of times the data was taken
        self._data = [] # nested list of all the data unfiltered
        self.satelliteId = np.zeros(32) #array of satelitteId found in chronological
        self._datasizes = np.zeros(365)
        #counters
        self.nr_satID = 0
        self.nr_datapoints = 0
        self.nr_datasets = 0

    def read_textfile(self,textfile,):
        """
        read textfile specified in the input and extract data from the data
        """

        with open(textfile+".txt", 'r') as infile:
            self.textfile = textfile
            for line in infile:
                if not line[0] == "%" and not line[0] == "#":
                    numbers = line.split(" ")
                    if len(numbers) == 7:
                        self._epochs.append([int(float(i)) for i in numbers])
                        self._datasizes[self.nr_datasets] = float(numbers[-1])
                        self.nr_datasets += 1
                    elif len(numbers) > 7:
                        # print(np.sum([numbers[0]== i for i in self.satelliteId]))
                        if sum([float(numbers[0])==i for i in self.satelliteId])==0:
                            self.satelliteId[self.nr_satID] = numbers[0]
                            self.nr_satID += 1
                        # print(numbers)

                        self._data.append(numbers)
                        self.nr_datapoints+=1
                        # print ("Perfectly balanced as all thing should be")
                    else:
                        raise ValueError("non-readable data in the textfile")

        #return table_array
        # return self.x
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
    def satellite_Id(self):
        """
        return the satelitteId that the measurement was used.

        """
        self.check_read_data()
        return self.satelliteId[0:self.nr_satID]

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

    def plotting_disturbances(self):
        self.check_read_data()
        plt.plot()
        plt.xlabel("time")
        plt.ylabel("S4")
        plt.title("")
        plt.show()


if __name__ == '__main__':
    obj = ReadData()
    obj.read_textfile("data/example_data")
    obj.display_epochs()
    obj.display_location_satellite()
    obj.satellite_Id
