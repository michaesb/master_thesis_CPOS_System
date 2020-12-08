import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

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
    x_min, x_max = -1, 30
    plt.subplot(3,1,1)
    plt.plot(days_magnetometer,magnetometer_values, "r")
    plt.plot(filtered_days,filtered_mag, "b")
    plt.plot(days_event+time_of_event/24,np.zeros(len(dates_event)), "g*")
    plt.title("Magnetometer,B_Z values and AE-index over 2018")
    plt.legend(["original", "filtered"])
    plt.ylabel("Magnetometer [nT]")
    plt.grid("on")
    plt.xticks([])
    plt.axis([x_min, x_max, -300, 300])
    #plotting B_z
    plt.subplot(3,1,2)
    plt.plot(days_hour[B_z>0], B_z_positive,"r", linewidth =0.4)
    plt.plot(days_hour[B_z<0], B_z_negative, "g")
    plt.plot(days_hour, np.zeros_like(days_hour), "r", linewidth=0.4)
    plt.axis([x_min, x_max, -20, 20])
    plt.grid("on")
    plt.xticks([])
    plt.ylabel("B_z-values [nT]")
    #plotting AE index
    plt.subplot(3,1,3)
    plt.plot(days_hour[1:], AE)
    #plt.title(" over 2018")
    plt.ylabel("AE-index [nT]")
    plt.xlabel("t [days]")
    plt.axis([x_min, x_max, 0, 1600])
    # plt.xticks([0,,9,14,19,24,29,34,39,44,49,54,59])
    plt.grid("on")
    plt.show()


obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()
obj_OMNI = ReadOMNIData()


try:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"
    path_OMNI = laptop_path+"OMNI_HRO_1MIN_179769.csv"
    path_AE = laptop_path+ "20201025-17-57-supermag_AE.csv"
    AE_dataframe = pd.read_csv(path_AE,names=["Date_UTC","SML","AE"], )
                               #na_values = {"AE":0})
except FileNotFoundError:
    pass

#     print("substorm event reader")
#     obj_event.read_csv(path_event,verbose = False)
#     print("magnetometer reader")
#     obj_mag.read_csv(path_mag, verbose = False)
#     print("substorm event reader")
#     obj_OMNI.read_csv(path_OMNI, verbose = False)
# #
# except FileNotFoundError:
#     desktop_path = "/run/media/michaelsb/HDD Linux/data/"
#     path_event = desktop_path+"substorm_event_list_2018.csv"
#     path_mag = desktop_path+"20201025-17-57-supermag.csv"
#     path_OMNI = desktop_path+"OMNI_HRO_1MIN_179769.csv"
#     path_AE = desktop_path+ "20201025-17-57-supermag_AE.csv"
#     print("substorm event reader")
#     obj_event.read_csv(path_event,verbose = False)
#     print("magnetometer reader")
#     obj_mag.read_csv(path_mag, verbose = False)
#     print("substorm event reader")
#     obj_OMNI.read_csv(path_OMNI, verbose = False)
#
#
# #magnetometer reader
# dates_mag, time_UTC_mag,\
# location_long,location_lat,\
# geographic_north,geographic_east, geographic_z, \
# magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("TRO")
#
# #then event reader
# lat = obj_event.latitude
# mag_time = obj_event.magnetic_time
# time_UTC_event = obj_event.dates_time
# dates_event, year = obj_event.day_of_year
#
# Norway_time = time_UTC_event + 1
# lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)
#
# #then OMNI_data
# B_z = obj_OMNI.ACE_B_z

AE = np.array(AE_dataframe["AE"].tolist()[1:])
SML = np.array(AE_dataframe["SML"][1:].tolist()[1:])
print(AE)
print(SML)
plt.plot(SML)
plt.plot(AE)
plt.show()
t_OMNI = obj_OMNI.time
dates, uneeded_info = obj_OMNI.day_of_year
days = date_to_days(dates)
days_hour = days + t_OMNI/24.

B_z_positive = B_z[B_z>0]
B_z_negative = B_z[B_z<0]


plot_single_event(dates_mag,dates_event, time_of_event,time_UTC_mag ,magnetic_north)
