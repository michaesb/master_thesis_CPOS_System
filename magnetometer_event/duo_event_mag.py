import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
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


def filtering_to_Norway_night(latitude, magnetic_time,time_UTC,dates,verbose=False):
    """
    filtering out the substorm event data to find the ones in Norway.
    """
    N =len(latitude)
    ind_arr = np.ones(N)
    #filtering out magnetic time that is not in the night
    ind_arr_1 = np.where(evening_time > magnetic_time,0, ind_arr)
    ind_arr_2 = np.where(morning_time < magnetic_time,0,ind_arr)
    ind_arr = np.where(ind_arr_1 +ind_arr_2 != 0, 1, np.nan)

    #filtering out the day UTC time
    ind_arr_3 = np.where(evening_time > time_UTC, 0,ind_arr)
    ind_arr_4 = np.where(morning_time < time_UTC, 0, ind_arr)
    ind_arr = np.where(ind_arr_3 +ind_arr_4 != 0, 1, np.nan)
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

def plot_substorm_days(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    print(days_event,len(days_event))
    days_magnetometer = date_to_days(dates_mag)
    filtered_mag = np.zeros(N_mag)*np.nan
    filtered_days = np.zeros(N_mag)*np.nan
    time_stamp_event = np.zeros(N_mag)*np.nan
    for i in range(N_mag):
        if days_magnetometer[i] in days_event:
            filtered_mag[i] = magnetometer_values[i]
            filtered_days[i] = days_magnetometer[i]


    days_magnetometer+=time_UTC_mag/24
    filtered_days+=time_UTC_mag/24

    plt.plot(days_magnetometer[:int(N_mag/4)],magnetometer_values[:int(N_mag/4)], "r")
    plt.plot(filtered_days[:int(N_mag/4)],filtered_mag[:int(N_mag/4)], "b")
    plt.plot(days_event[:int(N_event/8)]+time_of_event[:int(N_event/8)],np.ones(len(dates_event))[:int(N_event/8)], "g*")
    plt.title("North to south mag values before and after filtered")
    plt.legend(["original", "filtered"])
    plt.ylabel("B-values [nT]")
    plt.xlabel("day of year")
    plt.show()

obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()

try:
    path_event = "/scratch/michaesb/substorm_event_list_2018.csv"
    obj_event.read_csv(path_event)
    path_mag = "/scratch/michaesb/20201025-17-57-supermag.csv"
    obj_mag.read_csv(path_mag, verbose = True)
except FileNotFoundError:
    path_event = "/run/media/michaelsb/HDD Linux/data/substorm_event_list_2018.csv"
    path_mag = "/run/media/michaelsb/HDD Linux/data/20201025-17-57-supermag.csv"
    obj_mag.read_csv(path_mag, verbose = True)
    obj_event.read_csv(path_event)


#magnetometer reader

dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("DON")

#then event reader
evening_time = 20
morning_time = 4

lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)
# plot_latitude_time(lat,time_of_event, Norway_time,dates_event)

plot_substorm_days(dates_mag,dates_event, time_of_event,time_UTC_mag ,magnetic_north)
