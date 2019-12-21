import numpy as np
import matplotlib.pyplot as plt

class ReadData():
    def __init__(self,):
        self.textfile = "not an actual textfile"
        self.x = -1
    def read_textfile(self,textfile,year):
        with open(textfile+".txt", 'r') as data:
            #reading the first line and getting info about the structure of the textfile
            # print (data)
            self.textfile = textfile
            counter = 0
            for i in range(62):
                print( data.readline()[0:4])
                if not data.readline()[0:4] == "2018" or counter:
                    pass
                else:
                    counter = 1
                    first_line = data.readline()
                    print(first_line)
                    info = first_line.split()
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
