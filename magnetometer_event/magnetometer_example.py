import numpy as np
import matplotlib.pyplot as plt
import sys, time

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData


def plot_latitude_time(dates, mag_nt):
    """
    For investigating the magnetometer values, as it had missing data that needed
    to be filled.
    """
    days = date_to_days(dates)
    start_date = 8
    end_date = 9

    actual_days = np.linspace(1, 366, 24 * 60 * 365)

    for i in range(start_date * 24 * 60, end_date * 24 * 60):
        # print(magnetic_north[i])
        time.sleep(0.01)
        if magnetic_north[i] == np.nan:
            print(days[i], magnetic_north)
            print("------------------------------")
            # time.sleep(0.1)

    plt.plot(np.linspace(1, 366, 24 * 60 * 365), "b")
    plt.plot(days, "r")
    plt.show()
    plt.plot(
        (days[start_date * 60 * 24 : end_date * 60 * 24]) * 24,
        magnetic_north[start_date * 60 * 24 : end_date * 60 * 24],
        ".-",
    )
    plt.grid("on")
    plt.ylabel("magnetic north [nT]")
    plt.xlabel("day of year")
    plt.show()


obj_mag = ReadMagnetomerData()

save_ram_memory = False

try:
    file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
    path_mag = "/scratch/michaesb/20201025-17-57-supermag.csv"
    if save_ram_memory:
        with open(file_path, "rb") as file:
            time_UTC_mag = np.load(file, allow_pickle=True)
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
    path_mag = "/run/media/michaelsb/data_ssd/data/20201025-17-57-supermag.csv"
    file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
    if save_ram_memory:
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

plot_latitude_time(dates_mag, magnetic_north)
