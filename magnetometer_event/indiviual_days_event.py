import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys, time
from numba import njit, prange
from collections import Counter
import pandas as pd

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData
from noise_gps_function import run_NMEA_data
from ROTI_bilinear_interpolation import full_year_ROTI_bilinear_interpolation


def plot_all_days_tagged_events(
    gps_noise,
    gps_time,
    magnetic_north,
    time_UTC_mag,
    time_of_event,
    time_ROTI,
    ROTI_biints,
):
    borders = -250, -450

    hour_area = 4
    station = "TRM"
    for i in range(len(gps_time[:, 0])):
        gps_time[i, :] = gps_time[i, :] / 24 + i
    fig, ax = plt.subplots(3, 1, sharex=True)
    # np.nanmedian()
    # ax[0].plot(gps_time.flatten()[::],gps_noise.flatten()[::])
    ax[0].plot(time_UTC_mag, magnetic_north)
    ax[0].plot(time_of_event, np.zeros(len(time_of_event)), "r*", linewidth=0.5)
    ax[0].plot(time_UTC_mag, np.ones(len(magnetic_north)) * borders[0], alpha=0.4)
    ax[0].plot(time_UTC_mag, np.ones(len(magnetic_north)) * borders[1], alpha=0.4)
    ax[0].set_ylabel("Magnetic North [nT]")
    ax[0].set_title(
        "Magnetometer values with substorm event times, \n ROTI values and \n noise from gps at Tromsø in 2018"
    )
    ax[0].set_ylim(-1000, 400)
    ax[0].grid("on")

    ax[1].plot(time_ROTI, ROTI_biints, ".-")
    ax[1].set_ylabel("ROTI [TEC/min]")
    ax[1].grid("on")
    ax[2].plot(gps_time.flatten()[::4] + 1, gps_noise.flatten()[::4], ".")

    ax[2].plot(
        np.ones(2000) * gps_time.flatten()[start_index_weird_time],
        np.linspace(0, 1, 2000),
        alpha=0.5,
    )
    ax[2].plot(
        np.ones(2000) * gps_time.flatten()[end_index_weird_time],
        np.linspace(0, 1, 2000),
        alpha=0.5,
    )
    ax[2].set_yscale("log")
    ax[2].set_xlabel("days")
    # ax[0].set_ylim(5e-5,1e-1)
    ax[2].set_ylabel("GPS noise [m]")
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
        with open(file_path, "rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        (
            dates_mag,
            location_long,
            location_lat,
            geographic_north,
            geographic_east,
            geographic_z,
            magnetic_north,
            magnetic_east,
            magnetic_z,
        ) = obj_mag.receiver_specific_data(station)

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/data_ssd/data"
    path_event = desktop_path + "/substorm_event_list_2018.csv"
    path_mag = desktop_path + "/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)
    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path, "rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        (
            dates_mag,
            location_long,
            location_lat,
            geographic_north,
            geographic_east,
            geographic_z,
            magnetic_north,
            magnetic_east,
            magnetic_z,
        ) = obj_mag.receiver_specific_data(station)

########################### magnetometer reader  ##########################

stations_dictionary_GEO_coord = {
    "KIL": [69.02, 20.79],
    "TRM": [69.66, 18.94],  # 0  -0.01
    "ABK": [68.35, 18.82],
    "AND": [69.30, 16.03],
    "DOB": [62.07, 9.11],
    "DON": [66.11, 12.50],
    "JCK": [66.40, 16.98],
    "KAR": [59.21, 5.24],
    "MAS": [69.46, 23.70],
    "NOR": [71.09, 25.79],
    "RVK": [64.94, 10.99],
    "SOL": [61.08, 4.84],
    "SOR": [70.54, 22.22],
}

########################## event reader  #############################
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year
dates_event = pd.to_datetime(dates_event, format="%Y-%m-%d %H:%M:%S")
Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(
    lat, mag_time, Norway_time, dates_event
)

######################### ROTI data #####################################


def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path, "rb") as file:
        time = np.load(file)
        ROTI_biint = np.load(file)
    return time, ROTI_biint


time_ROTI, ROTI_biint_TRO = load_ROTI_data()

########################## gps noise  ##################################
def statistical_reduction_of_data(gps_data, start_index, end_index):
    originial_shape = gps_data.shape
    gps_data = gps_data.flatten()
    print(gps_data[start_index:end_index])
    median1 = np.nanmedian(gps_data[start_index:end_index])
    median2 = np.nanmedian(gps_data[:start_index])
    ratio = median1 / median2
    print("ratio", ratio)
    gps_data[start_index:end_index] = gps_data[start_index:end_index] / ratio
    gps_data = gps_data.reshape(365, 50500)
    return gps_data


def load_gps_noise():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path, "rb") as file:
        time = np.load(file)
        noise = np.load(file)
    start_index_weird_time = 7649115 - 50500
    end_index_weird_time = 7858915 - 50500
    noise = statistical_reduction_of_data(
        noise, start_index_weird_time, end_index_weird_time
    )
    return time, noise

    # return adjusted_gps_data


time_axis_gps, gps_noise = load_gps_noise()

start_index_weird_time = 7649115
end_index_weird_time = 7858915

################### Conversion or adjustment of different arrays ###############
time_mag = date_to_days(dates_mag)
time_of_event = date_to_days(dates_event) + mag_time / 24
# print(time_of_event)
###########################plotting different data ##########################
plot_all_days_tagged_events(
    gps_noise,
    time_axis_gps,
    magnetic_north,
    time_mag,
    time_of_event,
    time_ROTI,
    ROTI_biint_TRO,
)
