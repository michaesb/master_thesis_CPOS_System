import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys, time
from numba import njit, prange
from collections import Counter

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData
from magnetometer_event.creating_bins import create_bins_with_noise_sort, create_bins_gps_ROTI_mag
from noise_gps_function import run_NMEA_data
from ROTI_bilinear_interpolation import full_year_ROTI_bilinear_interpolation


def plot_all_days_tagged_events(gps_noise, gps_time,magnetic_north,time_UTC_mag,\
                                time_of_event,time_ROTI,ROTI_biints):
    borders = -250,-450

    hour_area = 4
    station = "TRM"
    for i in range(len(gps_time[:,0])):
        gps_time[i,:] = gps_time[i,:]/24+i
    fig,ax = plt.subplots(3,1, sharex = True)
    # np.nanmedian()
    # ax[0].plot(gps_time.flatten()[::],gps_noise.flatten()[::])
    ax[0].plot(time_UTC_mag,magnetic_north)
    ax[0].plot(time_of_event,np.zeros(len(time_of_event)), "r*", linewidth =0.5)
    ax[0].plot(time_UTC_mag, np.ones(len(magnetic_north))*borders[0],alpha=0.4)
    ax[0].plot(time_UTC_mag, np.ones(len(magnetic_north))*borders[1],alpha=0.4)
    ax[0].set_ylabel("North component B-value [nT]")
    ax[0].set_title("magnetometer values with substorm trigger, \n ROTI values and \n noise from gps at Tromsø in 2018")
    ax[0].set_ylim(-1000,400)
    ax[0].grid("on")

    ax[1].plot(time_ROTI,ROTI_biints)
    ax[1].set_ylabel("ROTI [TEC/min]")
    ax[1].grid("on")
    ax[1].set_xlabel("days")


    ax[2].plot(gps_time.flatten()[::4]+1,gps_noise.flatten()[::4],'.')
    ax[2].set_yscale("log")
    # ax[0].set_ylim(5e-5,1e-1)
    ax[2].set_ylabel("noise values from the NMEA")
    ax[2].grid("on")

    plt.show()

obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()

save_ram_memory = True
station = "TRO"

try:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path + "substorm_event_list_2018.csv"
    path_mag = laptop_path + "20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)
    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path,"rb") as file:
            time_UTC_mag  = np.load(file, allow_pickle=True)
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        dates_mag,time_UTC_mag,location_long,location_lat,geographic_north,\
        geographic_east,geographic_z,magnetic_north,magnetic_east,magnetic_z\
        = obj_mag.receiver_specific_data(station)

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/data_ssd/data"
    path_event = desktop_path + "/substorm_event_list_2018.csv"
    path_mag = desktop_path + "/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)
    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path,"rb") as file:
            time_UTC_mag  = np.load(file, allow_pickle=True)
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        dates_mag,time_UTC_mag,location_long,location_lat,geographic_north,\
        geographic_east,geographic_z,magnetic_north,magnetic_east,magnetic_z\
        = obj_mag.receiver_specific_data(station)

########################### magnetometer reader  ##########################

stations_dictionary_GEO_coord = {"KIL": [69.02, 20.79],"TRM": [69.66, 18.94], #0  -0.01
"ABK": [68.35, 18.82],"AND": [69.30, 16.03],"DOB": [62.07, 9.11],
"DON": [66.11, 12.50],"JCK": [66.40, 16.98],"KAR": [59.21, 5.24],
"MAS": [69.46, 23.70],"NOR": [71.09, 25.79],"RVK": [64.94, 10.99],
"SOL": [61.08, 4.84],"SOR": [70.54, 22.22],}

########################## event reader  #############################
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(
lat, mag_time, Norway_time, dates_event)

########################## gps noise  ##################################

def create_fake_noise():
    n = 50200
    time_axis_gps = np.zeros((365, n + 365)) * np.nan
    gps_noise = np.zeros((365, n + 365)) * np.nan
    for i in range(365):
        time_axis_gps[i, : n + i] = np.linspace(0, 24, n + i)
        gps_noise[i, : n + i] = np.random.random(n + i)
    return time_axis_gps, gps_noise

def load_gps_noise():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        time = np.load(file)
        noise = np.load(file)
    return time, noise

time_axis_gps,gps_noise = load_gps_noise()

# time_axis_gps,gps_noise = run_NMEA_data(365,"TRM")
# time_axis_gps, gps_noise = create_fake_noise()
######################### ROTI data #####################################


def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"rb") as file:
        time = np.load(file)
        ROTI_biint = np.load(file)
    return time, ROTI_biint

time_ROTI, ROTI_biint_TRO = load_ROTI_data()


########################## creating bins ###################################

# bins_sorted,time_day_bins,time_of_event,events_collection_sorted,ROTI_event_sorted,noise_gps_sorted \
# = create_bins_with_noise_sort(dates_mag,dates_event,Norway_time,
#                               time_UTC_mag,magnetic_north,
#                               gps_noise,time_axis_gps,
#                               time_ROTI_TRO, ROTI_biint_TRO)
# = create_bins_gps_ROTI_mag(dates_mag,dates_event,Norway_time,
# time_UTC_mag,magnetic_north,
# gps_noise,time_axis_gps,
# time_ROTI_TRO, ROTI_biint_TRO)



################### Conversion or adjustment of different arrays ###############
days_magnetometer = date_to_days(dates_mag)
days_event = date_to_days(dates_event)

time_of_event = days_event + mag_time/24
time_mag = days_magnetometer + time_UTC_mag/24.

###########################plotting different data ##########################
plot_all_days_tagged_events(gps_noise,time_axis_gps,magnetic_north,time_mag,\
time_of_event,time_ROTI,ROTI_biint_TRO)
