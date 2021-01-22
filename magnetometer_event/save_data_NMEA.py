import numpy as np
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from noise_gps_function import run_NMEA_data

time_axis_gps,gps_noise = run_NMEA_data(365,"TRM")
file_path = "../../data_storage_NMEA/NMEA_data_TRM.txt"
with open(file_path,"wb") as file:
    np.save(file,time_axis_gps)
    np.save(file,gps_noise)
with open(file_path,"rb") as file:
    a = np.load(file)
    b = np.load(file)

print(a)
print(b)
