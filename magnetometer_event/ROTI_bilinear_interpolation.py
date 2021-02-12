 #!/usr/bin/env python3
import time, sys, os, unittest
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_ROTI.ROTI_data_reader import ReadROTIData
from mpl_toolkits.axes_grid1 import make_axes_locatable

def check_coordinates_system(x_axis,y_axis):
    """
    Checks that the coordinates given in the data for each file is the same
    """
    standard_x_axis = [-70.,40.,1.]
    standard_y_axis = [50.,80.,1.]
    if standard_y_axis == y_axis and standard_x_axis == x_axis:
        pass
    else:
        print("dimension errors in the axis from the data")
        exit()

def bilinear_interpolation(x,y,x_,y_,val):
    a = 1 /((x_[1] - x_[0]) * (y_[1] - y_[0]))
    xx = np.array([[x_[1]-x],[x-x_[0]]],dtype='float32')
    f = np.array(val).reshape(2,2)
    yy = np.array([[y_[1]-y],[y-y_[0]]],dtype='float32')
    b = np.matmul(f,yy)
    return a * np.matmul(xx.T, b)[[0]]


def extract_day_data(month,date,station_coordinates):
    year = "2018"
    adress_folder = "/run/media/michaelsb/data_ssd/data/RTIM/"+year+"/"+month+"/"+date+"/ROTI/"
    date = adress_folder[40:44] +adress_folder[45:47]+adress_folder[48:50]
    date_plotting_path = adress_folder[40:44] +"/"+adress_folder[45:47]+"/"+adress_folder[48:50]
    date_folder = "ROTI_" +date_plotting_path+"/"
    folder_path = "../plots/" + date_folder
    adresses = []
    ROTI_Ground_mag_station = np.zeros((24,12))*np.nan
    ROTI_time = np.zeros((24,12))*np.nan
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
            tqdm.write(f"FileNotFoundError {adresses[i]}")
            continue

        x_axis,y_axis = ROTI_data.coordinates[0],ROTI_data.coordinates[1]
        data = ROTI_data.ROTI_Grid_data

        if len(ROTI_data.time)!=12:
            for k in range(len(ROTI_data.time)):
                ROTI_time[i,k]=ROTI_data.time[k]/60 + i
        else:
            ROTI_time[i,:] = np.array(ROTI_data.time)/60 + i
        check_coordinates_system(x_axis,y_axis) #A test of the axis in the ROTI data

        latitude_station, longitude_station = station_coordinates
        index_x, index_y = longitude_station-x_axis[0],y_axis[1]-latitude_station
        index_x_ceil, index_x_floor = int(np.ceil(index_x)), int(np.floor(index_x))
        index_y_ceil, index_y_floor = int(np.ceil(index_y)), int(np.floor(index_y))
        # print(index_y,latitude_station)
        # print(index_y_ceil,index_y_floor)
        for ii in range(len(data[0,0,:])):
            Q_values = [data[index_y_floor,index_x_floor,ii], data[index_y_floor,index_x_ceil,ii],\
                        data[index_y_ceil,index_x_floor,ii], data[index_y_ceil,index_x_ceil,ii]]
            data[index_y_floor-1,index_x_floor-1,ii]=100
            data[index_y_floor-1,index_x_ceil+1,ii]=100
            data[index_y_ceil+1,index_x_floor-1,ii]=100
            data[index_y_ceil+1,index_x_ceil+1,ii]=100

            ROTI_Ground_mag_station[i,ii] = bilinear_interpolation(x=index_x, y=index_y,
                                                    x_=[index_x_floor,index_x_ceil],
                                                    y_=[index_y_floor,index_y_ceil],
                                                    val=Q_values)
    return ROTI_time, ROTI_Ground_mag_station

def dates_of_year_2018():
    months = []
    dates = []
    day_in_a_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    for i in range(len(day_in_a_month)):
        for ii in range(1,day_in_a_month[i]+1):
            if len(str(i+1))==1:
                if len(str(ii))==1:
                    month = f"0{i+1}"
                    date = f"0{ii}"
                    months.append(month)
                    dates.append(date)

                else:
                    month = f"0{i+1}"
                    date = f"{ii}"
                    dates.append(date)
                    months.append(month)
            else:
                if len(str(ii))==1:
                    month = f"{i+1}"
                    date = f"0{ii}"
                    months.append(month)
                    dates.append(date)
                else:
                    month = f"{i+1}"
                    date = f"{ii}"
                    months.append(month)
                    dates.append(date)
    return dates, months

def full_year_ROTI_bilinear_interpolation(coordinates, unit_days=False):
    dates, months = dates_of_year_2018()
    full_year_dataaset_ROTI = np.zeros(12*24*len(dates))*np.nan
    full_year_dataaset_time = np.zeros(12*24*len(dates))*np.nan

    for i in tqdm(range(len(dates)),desc = "ROTI bilinear_interpolation full year"):
        tqdm.write(f"{months[i]}/{dates[i]}")
        time,ROTI_coordinates_data = extract_day_data(months[i],dates[i],coordinates)
        full_year_dataaset_ROTI[12*24*i:12*24*(i+1)] = ROTI_coordinates_data.flatten()
        if unit_days == True:
            full_year_dataaset_time[12*24*i:12*24*(i+1)] = time.flatten()/24+i+1
        else:
            full_year_dataaset_time[12*24*i:12*24*(i+1)] = time.flatten()

    return full_year_dataaset_time, full_year_dataaset_ROTI

def plot_full_year_ROTI_bilinear_interpolation(coordinates):
    time,ROTI_val = full_year_ROTI_bilinear_interpolation(coordinates)
    
    for i in range(int(len(time)/(12*24))):
        plt.plot(time[12*24*i:12*24*(i+1)],ROTI_val[12*24*i:12*24*(i+1)])

    plt.title(f"ROTI data at Tromso magnetometer station \n coordinates:\
    {coordinates[:]} Full year 2018")
    plt.xlabel("time of day [hour]")
    plt.ylabel("ROTI value [TEC/min]")
    plt.show()

if __name__ == '__main__':
    TRO = [69.66, 18.94]
    try:
        month, date = sys.argv[1][0:2], sys.argv[1][2:]
        print("month",month,"date",date)
        time,ROTI_TRO_data = extract_day_data(month,date,TRO)
        plt.plot(time.flatten(),ROTI_TRO_data.flatten())
        plt.title(f"ROTI data at Tromso magnetometer station \n coordinates: {TRO[:]}\
        date:{date}/{month}/2018")
        plt.xlabel("time of day [hour]")
        plt.ylabel("ROTI value [TEC/min]")
        plt.show()
    except IndexError:
        print("full year of 2018")
        plot_full_year_ROTI_bilinear_interpolation(TRO)
