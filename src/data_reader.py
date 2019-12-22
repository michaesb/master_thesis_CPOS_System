import numpy as np
import matplotlib.pyplot as plt

class ReadData():
    def __init__(self,):
        self.textfile = "not an actual textfile"
        self.x = -1
        self.epochs = []

    def read_textfile(self,textfile,year):
        with open(textfile+".txt", 'r') as data:
            #reading the first line and getting info about the structure of the textfile
            # print (data)
            self.textfile = textfile
            counter = 0
            for line in data:
                if not line[0] == "%" and not line[0] == "#":
                    numbers = line.split(" ")
                    if len(numbers) == 7:
                        self.epochs.append([int(float(i)) for i in numbers])
                    elif len(numbers)
                        print ("Perfectly balanced as all thing should be")
                    else:
                        raise ValueError("non-readable data in the textfile")
            print(self.epochs)

            """
            if format == "colon2":
                for line, i in zip(data,range(nr_lines)):
                    if line[0] !='#':
                        #print('line', line)
                        list = line.split(':')
                        #print('list', list)
                        array = np.array([float(j) for j in list])
                        table_array[i,:] = array
                        #print('table_array', table_array)
             """
        #return table_array
        return self.x

    def display_data(self,):
        print

if __name__ == '__main__':
    year = 2018
    obj = ReadData()
    obj.read_textfile("data/example_data", year)
