import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData

def plot_latitude_time(dates,time_UTC,mag_nt):
    days = date_to_days(dates) + time_UTC
    plt.plot(days[::20],magnetic_north[::20], "*")
    plt.ylabel("time of day")
    plt.xlabel("day of year")
    plt.show()

obj = ReadMagnetomerData()

try:
    path = "/scratch/michaesb/20201025-17-57-supermag.csv"
    obj.read_csv(path, verbose = True)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/20201025-17-57-supermag.csv"
    obj.read_csv(path, verbose = True)
t1= time.time()
dates,time_UTC,location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj.receiver_specific_data("DON")
print("time",time.time()-t1)
print(dates)
plot_latitude_time(dates, time_UTC, magnetic_north)
