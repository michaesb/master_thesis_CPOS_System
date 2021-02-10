import numpy as np
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from noise_gps_function import run_NMEA_data
from ROTI_bilinear_interpolation import full_year_ROTI_bilinear_interpolation

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
    time,ROTI_biint = full_year_ROTI_bilinear_interpolation(TRO, unit_days=True)
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"wb") as file:
        np.save(file,time)
        np.save(file,ROTI_biint)

def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"rb") as file:
        a = np.load(file)
        b = np.load(file)

    print(a)
    print(b)

ROTI_save_data()
load_ROTI_data()
