 #!/usr/bin/env python3
import time, sys, os, unittest
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_ROTI.ROTI_data_reader import ReadROTIData

def check_coordinates_system(x_axis,y_axis):
    """
    Checks that the coordinates given in the data for each file is the same
    """
    standard_x_axis = [-70.,40.,1.]
    standard_y_axis = [50.,80.,1.]
    if standard_y_axis == y_axis and standard_x_axis == x_axis:
        pass
    else:
        print("dimension errors")
        exit()

def bilinear_interpolation(x,y,x_,y_,val):

    a = 1 /((x_[1] - x_[0]) * (y_[1] - y_[0]))
    xx = np.array([[x_[1]-x],[x-x_[0]]],dtype='float32')
    f = np.array(val).reshape(2,2)
    yy = np.array([[y_[1]-y],[y-y_[0]]],dtype='float32')
    b = np.matmul(f,yy)

    return a * np.matmul(xx.T, b)

bilinear_interpolation(x=54.4786674627,
                       y=17.0470721369,
                       x_=[54.458333,54.5],
                       y_=[17.041667,17.083333],
                       val=[31.993,31.911,31.945,31.866])

def extract_day_data(month,date,station_coordinates):
    date = adress_folder[40:44] +adress_folder[45:47]+adress_folder[48:50]
    date_plotting_path = adress_folder[40:44] +"/"+adress_folder[45:47]+"/"+adress_folder[48:50]
    date_folder = "ROTI_" +date_plotting_path+"/"
    folder_path = "../plots/" + date_folder

    adresses = []
    for i in range(24):
        if len(str(i))==1:
            adress_temp = adress_folder + "ROTI_"+ date +"_0"+str(i)+"00to0"+str(i)+"59.txt"
            adresses.append(adress_temp)
        else:
            adress_temp = adress_folder + "ROTI_"+ date +"_"+str(i)+"00to"+str(i)+"59.txt"
            adresses.append(adress_temp)
    for i in range(len(adresses)):
        ROTI_data = ReadROTIData()
        try:
            ROTI_data.read_textfile(adresses[i], False)
        except FileNotFoundError:
            print("FileNotFoundError"+str(adresses[i]))
            continue
        if i == 0:
            print("longitude, latitude", ROTI_data.coordinates)

        x_axis,y_axis = ROTI_data.coordinates[0],ROTI_data.coordinates[1]
        data = ROTI_data.ROTI_Grid_data
        time_of_grid = ROTI_data.time
        check_coordinates_system(x_axis,y_axis) #A test of the axis in the ROTI data
        latitude_station, longitude_station = station_coordinates
        index_x, index_y = longitude_station-x_axis[0],latitude_station-y_axis[0]
        index_x_0, index_x_1 = np.ceil(index_x), np.floor(index_x)
        index_y_0, index_y_1 = np.ceil(index_y), np.floor(index_y)
        print(x_axis,longitude_station)
        print("index_x",index_x_0,index_x_1)
        print(y_axis,latitude_station)
        print("index_y",index_y_0,index_y_1)
        print(station_coordinates)
        Q =
        exit()

if __name__ == '__main__':
    try:
        month, date = sys.argv[1][0:2], sys.argv[1][2:]
        print("month",month,"date",date)
        adress_folder = "/run/media/michaelsb/data_ssd/data/RTIM/2018/"+month+"/"+date+"/ROTI/"
    except:
        print("give arguments to the program")
        exit()
    TRO = [69.66, 18.94]
    extract_day_data(month,date,TRO)
