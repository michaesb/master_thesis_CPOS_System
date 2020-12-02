import numpy as np
import matplotlib.pyplot as plt
import sys, time
from collections import Counter
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

def create_bins(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    filtered_mag = np.zeros(N_mag)*np.nan
    filtered_days = np.zeros(N_mag)*np.nan
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)
    time_day_bins = np.zeros(N_event)
    j=0
    date = 0
    for i in range(N_mag):
        if days_magnetometer[i] in days_event:
            filtered_mag[i] = magnetometer_values[i]
            filtered_days[i] = days_magnetometer[i]
            if date != days_magnetometer[i]:
                date = days_magnetometer[i]
                for k in range(Counter(days_event)[days_magnetometer[i]]):
                    hour_area = 2
                    index_min, index_max = i+int(time_of_event[j] - hour_area/2)*60\
                                          ,i+int(time_of_event[j] + hour_area/2)*60
                    bin_value = np.min(magnetometer_values[index_min:index_max])
                    if bin_value !=bins[j-1]:
                        bins[j] = bin_value
                        time_day_bins[j] = days_magnetometer[i]+time_of_event[j]/24
                    else:
                        bins[j] = np.nan
                        time_day_bins[j] = np.nan

                    print("----- \nindex",j, "date of event trigger ",date,)
                    print("minimal value",bin_value,"time of event",time_of_event[j])
                    print("for loop k ",k)
                    print("-----")
                    j+=1

    plt.hist(bins, bins = 30)
    plt.title("2018, Tromso,\n Max magnetometer value of a substorm event")
    plt.xlabel("minimum of the north component magnetometer [nT]")
    plt.ylabel("number of occurances")
    plt.show()
    plt.hist(time_day_bins, bins = 30)
    plt.title("Time of year when the substorm occurs")
    plt.xlabel("day of year")
    plt.ylabel("number of occurances")
    plt.show()
    plt.hist(time_of_event, bins = 80)
    plt.title("Distrubution of what time the substorm occurs")
    plt.xlabel("time of day [UT+1]")
    plt.show()

    """
    days_magnetometer+=time_UTC_mag/24
    filtered_days+=time_UTC_mag/24
    plt.plot(days_magnetometer,magnetometer_values, "r")
    plt.plot(filtered_days,filtered_mag, "b")
    plt.plot(days_event+time_of_event/24,np.zeros(N_event), "*g", markersize = 10)
    plt.title("North to south mag values before and after filtered")
    x_min,x_max =7, 15
    # plt.axis([x_min, x_max, -50, 50])
    plt.legend(["original", "filtered"])
    plt.ylabel("B-values [nT]")
    plt.xlabel("day of year")
    plt.grid("on")
    plt.show()
    """

obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()

try:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"

    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/HDD Linux/data/"
    path_event = desktop_path+"/substorm_event_list_2018.csv"
    path_mag = desktop_path+"/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")


#magnetometer reader
dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("TRO")

#then event reader
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

create_bins(dates_mag,dates_event, Norway_time,time_UTC_mag ,magnetic_north)
