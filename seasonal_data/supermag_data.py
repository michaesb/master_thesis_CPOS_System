import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent

def plot_latitude_time(latitude,mag_time,time_UTC,dates):
    days = date_to_days(dates)
    plt.subplot(3,1,1)
    plt.plot(days,latitude, "*")
    plt.title("Substorm data plotted with "+ str(len(latitude))+ " points")
    plt.ylabel("latitude")
    plt.xticks([])
    plt.subplot(3,1,2)
    plt.plot(days,mag_time, "*")
    plt.ylabel("time of day")
    plt.xticks([])
    plt.subplot(3,1,3)
    plt.plot(days,time_UTC, "*")
    plt.ylabel("time of day")
    plt.xlabel("day of year")
    plt.show()


def filtering_to_Norway_night(latitude, magnetic_time,time_UTC,dates,N,verbose=False):
    ind_arr = np.ones(len(latitude))

    #filtering out magnetic time that is not in the night
    ind_arr_1 = np.where(evening_time > magnetic_time,0, ind_arr)
    ind_arr_2 = np.where(morning_time < magnetic_time,0,ind_arr)
    ind_arr = np.where(ind_arr_1 +ind_arr_2 != 0, 1, np.nan)

    #filtering out the day UTC time
    ind_arr_3 = np.where(evening_time > time_UTC, 0,ind_arr)
    ind_arr_4 = np.where(morning_time < time_UTC, 0, ind_arr)
    ind_arr = np.where(ind_arr_3 +ind_arr_4 != 0, 1, np.nan)
    print(np.nansum(ind_arr))
    # filtering latitude that is not in Norway
    ind_arr = np.where(58 > latitude ,np.nan,ind_arr)
    ind_arr = np.where(latitude > 71,np.nan,ind_arr)
    latitude =latitude[np.logical_not(np.isnan(ind_arr))]
    magnetic_time =magnetic_time[np.logical_not(np.isnan(ind_arr))]
    time_UTC =time_UTC[np.logical_not(np.isnan(ind_arr))]
    dates = dates[np.logical_not(np.isnan(ind_arr))]
    if verbose:
        print("reduced from ",N, " to ", len(time_UTC), \
              "ratio:", 100*len(time_UTC)/N, " %")
    return latitude, magnetic_time, time_UTC, dates


obj = ReadSubstormEvent()

try:
    path = "/scratch/michaesb/substorm_event_list_2018.csv"
    obj.read_csv(path)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/substorm_event_list_2018.csv"
    obj.read_csv(path)

evening_time = 20
morning_time = 4

N = obj.datapoints
lat = obj.latitude
mag_time = obj.magnetic_time
time_UTC = obj.dates_time
date_UTC, year = obj.day_of_year

Norway_time = time_UTC + 1
plot_latitude_time(lat,mag_time, Norway_time,date_UTC)
lat, mag_time, Norway_time, dates = filtering_to_Norway_night(lat,mag_time,Norway_time,date_UTC,N,verbose=True)
plot_latitude_time(lat,mag_time, Norway_time,dates)
