import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData
from noise_gps_function import run_filter_plot_NMEA_data

def plot_single_event(dates_mag,dates_event, time_of_event, time_UTC_mag, \
                      magnetometer_values,date,noise,noise_21_3,noise_3_9):
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
    x_min, x_max = -1, 60
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
    fig,ax = plt.subplots(4,1, sharex = True)
    ax[0].plot(days_magnetometer,magnetometer_values, "r")
    ax[0].plot(filtered_days,filtered_mag, "b")
    ax[0].plot(days_event+time_of_event/24,np.zeros(len(dates_event)), "g*")
    ax[0].set_title("Magnetometer,B_Z values, AE-index and noise from GPS over 2018")
    ax[0].legend(["original", "filtered"])
    ax[0].set_ylabel("Magnetometer [nT]")
    ax[0].grid("on")
    ax[0].set_xticks(range(4,59,5))
    # ax[0].set_xticks([])
    ax[0].axis([x_min, x_max, -300, 300])
    #plotting B_z
    ax[1].plot(days_hour[B_z>0], B_z_positive,"r", )
    ax[1].plot(days_hour[B_z<0], B_z_negative, "g",)
    ax[1].plot(days_hour, np.zeros_like(days_hour), "r", linewidth=0.4)
    ax[1].axis([x_min, x_max, -20, 20])
    ax[1].grid("on")
    # ax[1].set_xticks([])
    ax[1].set_xticks(range(4,59,5))
    ax[1].set_ylabel("B_z-values [nT]")
    #plotting AE index
    ax[2].plot(days_hour, AE)
    ax[2].set_ylabel("AE-index [nT]")
    ax[2].axis([x_min, x_max, 0, 1600])
    ax[2].set_xticks(range(4,59,5))
    # ax[2].set_xticks([])
    ax[2].grid("on")
    ax[3].plot(date,noise_21_3[:,0], label=str(21)+"-"+str(23))
    ax[3].plot(date,noise_21_3[:,1], label=str(23)+"-"+str(1))
    ax[3].plot(date,noise_21_3[:,2], label=str(1)+"-"+str(3))
    for k in range(3):
        ax[3].plot(date,noise_3_9[:,k], label=str(3+2*k)+"-"+str(3+2*(k+1)))
    # ax[3].plot(date,noise[:,2], "blue", label="09-15")
    # ax[3].plot(date,noise[:,3], "black", label="15-21" )
    ax[3].set_ylabel("sample noise [m]")
    ax[3].set_xlabel("days")
    ax[3].grid("on")
    ax[3].set_xticks(range(4,x_max-1,5))
    ax[3].legend()
    plt.show()


obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()
obj_OMNI = ReadOMNIData()


try:
    desktop_path = "/run/media/michaelsb/HDD Linux/data/"
    path_event = desktop_path+"substorm_event_list_2018.csv"
    path_mag = desktop_path+"20201025-17-57-supermag.csv"
    path_OMNI = desktop_path+"OMNI_HRO_1MIN_179769.csv"
    print("substorm event reader")
    obj_event.read_csv(path_event,verbose = False)
    print("magnetometer reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("OMNI reader")
    obj_OMNI.read_csv(path_OMNI, verbose = False)


except FileNotFoundError:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"
    path_OMNI = laptop_path+"OMNI_HRO_1MIN_179769.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")
    obj_OMNI.read_csv(path_OMNI, verbose = False)
    print("OMNI reader")


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
lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

#then OMNI_data
B_z = obj_OMNI.ACE_B_z
AE = obj_OMNI.AE_index
t_OMNI = obj_OMNI.time
dates, uneeded_info = obj_OMNI.day_of_year
days = date_to_days(dates)
days_hour = days + t_OMNI/24.


receiver ="TRM"
nr_days = 60
year = "2018"

date,noise,noise_21_3,noise_3_9= run_filter_plot_NMEA_data(nr_days,receiver)


B_z_positive = B_z[B_z>0]
B_z_negative = B_z[B_z<0]


plot_single_event(dates_mag,dates_event, time_of_event,time_UTC_mag\
                 ,magnetic_north, date, noise, noise_21_3,noise_3_9)
