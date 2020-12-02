import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from magnetometer_event.filtering_events import filtering_to_Norway_night

def plot_latitude_time(latitude,mag_time,time_UTC,dates):
    xmin,x_max =4, 5
    days = date_to_days(dates)
    plt.subplot(3,1,1)
    plt.plot(days,latitude, "*")
    plt.title("Substorm data plotted with "+ str(len(latitude))+ " points")
    plt.ylabel("latitude")
    plt.xticks([])
    plt.subplot(3,1,2)
    plt.plot(days,mag_time, "*")
    plt.ylabel("time of day")
    plt.axis([x_min, x_max, -300, 300])
    plt.xticks([])
    plt.subplot(3,1,3)
    plt.plot(days,time_UTC, "*")
    plt.ylabel("time of day")
    plt.xlabel("day of year")
    plt.show()


def plot_substorm_days(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
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
    plt.plot(days_magnetometer,magnetometer_values, "r")
    plt.plot(filtered_days,filtered_mag, "b")
    plt.plot(days_event+time_of_event/24,np.zeros(len(dates_event)), "*g", markersize = 10)
    plt.title("North to south mag values before and after filtered")
    x_min,x_max =7, 15
    plt.axis([x_min, x_max, -50, 50])
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

lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)
# plot_latitude_time(lat,time_of_event, Norway_time,dates_event)

plot_substorm_days(dates_mag,dates_event, time_of_event,time_UTC_mag ,magnetic_north)
