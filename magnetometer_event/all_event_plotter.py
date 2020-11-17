import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

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

def plot_single_event(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
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
    plt.subplot(3,1,1)
    plt.plot(days_magnetometer,magnetometer_values, "r")
    plt.plot(filtered_days,filtered_mag, "b")
    plt.plot(days_event+time_of_event/24,np.zeros(len(dates_event)), "g*")
    plt.title("Magnetometer,B_Z values and AE-index over 2018")
    plt.legend(["original", "filtered"])
    plt.ylabel("B-values [nT]")
    plt.xticks([])
    plt.axis([x_min, x_max, -300, 300])


obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()
obj_OMNI = ReadOMNIData()


try:
    laptop_path = "/scratch/michaesb"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"
    path_OMNI = laptop_path+"OMNI_HRO_1MIN_179769.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")
    obj_OMNI.read_csv(path_OMNI, verbose = False)
    print("substorm event reader")

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/HDD Linux/data/"
    path_event = desktop_path+"/substorm_event_list_2018.csv"
    path_mag = desktop_path+"/20201025-17-57-supermag.csv"
    path_OMNI = desktop_path+"/OMNI_HRO_1MIN_179769.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")
    obj_OMNI.read_csv(path_OMNI, verbose = False)
    print("substorm event reader")


#magnetometer reader
dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("TRO")

#then event reader
evening_time = 20
morning_time = 4

lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

#then OMNI_data
B_z = obj_OMNI.ACE_B_z
AE = obj_OMNI.AE_index
t_OMNI = obj_OMNI.time
dates, uneeded_info = obj_OMNI.day_of_year
days = date_to_days(dates)
days_hour = days + t_OMNI/24.

B_z_positive = B_z[B_z>0]
B_z_negative = B_z[B_z<0]


x_min, x_max = -5, 65
plot_single_event(dates_mag,dates_event, time_of_event,time_UTC_mag ,magnetic_north)

plt.subplot(3,1,2)
plt.plot(days_hour[B_z>0], B_z_positive,"r", linewidth =0.4)
plt.plot(days_hour[B_z<0], B_z_negative, "g")
plt.plot(days_hour, np.zeros_like(days_hour), "r", linewidth=0.4)
plt.xticks([])
plt.ylabel("magnetic values [nT]")

plt.subplot(3,1,3)
plt.plot(days_hour, AE)
#plt.title(" over 2018")
plt.ylabel("magnetic values [nT]")
plt.xlabel("t [days]")
plt.axis([-15, 366, 0, 1600])
plt.show()
