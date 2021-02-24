import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData

def plot_latitude_time(dates,time_UTC,mag_nt):
    days = date_to_days(dates) + time_UTC/24.
    start_date=7+1
    end_date=8+1
    pseudo_days = np.linspace(1,366,len(days))
    print(dates[11812-2:11812+2])
    print(time_UTC[11812:11814])
    plt.plot(days -pseudo_days)
    plt.show()
    plt.plot((days[start_date*60*24:end_date*60*24]-start_date-1)*24,magnetic_north[start_date*60*24:end_date*60*24], ".-")
    plt.grid("on")
    plt.ylabel("time of day")
    plt.xlabel("day of year")
    plt.show()

obj_mag = ReadMagnetomerData()

save_ram_memory = False

try:
    file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
    path_mag = "/scratch/michaesb/20201025-17-57-supermag.csv"
    if save_ram_memory:
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
    path = "/run/media/michaelsb/HDD Linux/data/20201025-17-57-supermag.csv"
    obj.read_csv(path, verbose = True)

    dates,time_UTC,location_long,location_lat,\
    geographic_north,geographic_east, geographic_z, \
    magnetic_north,magnetic_east, magnetic_z = obj.receiver_specific_data("DON")
plot_latitude_time(dates_mag, time_UTC_mag, magnetic_north)
