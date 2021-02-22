import numpy as np
import sys, time

sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from noise_gps_function import run_NMEA_data
from ROTI_bilinear_interpolation import full_year_ROTI_bilinear_interpolation
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData

def NMEA_save_data():
    time_axis_gps,gps_noise = run_NMEA_data(365,"TRM")
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path,"wb") as file:
        np.save(file,time_axis_gps)
        np.save(file,gps_noise)

def load_NMEA_data():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        a = np.load(file)
        b = np.load(file)

    print(a)
    print(b)


def ROTI_save_data():
    TRO = [69.66, 18.94]
    time,ROTI_biint = full_year_ROTI_bilinear_interpolation(TRO)
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"wb") as file:
        np.save(file,time)
        np.save(file,gps_noise)

def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"rb") as file:
        a = np.load(file)
        b = np.load(file)

    print(a)
    print(b)

def magnetometer_save_data():
    obj_mag = ReadMagnetomerData()
    station = "TRO"
    file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
    try:
        laptop_path = "/scratch/michaesb/"
        path_mag = laptop_path + "20201025-17-57-supermag.csv"
        obj_mag.read_csv(path_mag, verbose=False)
    except FileNotFoundError:
        desktop_path = "/run/media/michaelsb/data_ssd/data"
        path_mag = desktop_path + "/20201025-17-57-supermag.csv"
        obj_mag.read_csv(path_mag, verbose=False)
    dates_mag,time_UTC_mag,location_long,location_lat,geographic_north,\
    geographic_east,geographic_z,magnetic_north,magnetic_east,magnetic_z\
    = obj_mag.receiver_specific_data(station)
    with open(file_path,"wb") as file:
        np.save(file,time_UTC_mag,allow_pickle= True)
        np.save(file,dates_mag, allow_pickle= True)
        np.save(file,magnetic_north, allow_pickle= True)


def load_magnetometer_data():
    file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
    with open(file_path,"rb") as file:
        a = np.load(file, allow_pickle=True)
        b = np.load(file, allow_pickle=True)
        c = np.load(file, allow_pickle=True)

    print(a)
    print(b)
    print(c)



# ROTI_save_data()
# load_ROTI_data()
magnetometer_save_data()
load_magnetometer_data()
