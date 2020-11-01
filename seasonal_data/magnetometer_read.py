import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData

def plot_latitude_time(latitude,mag_time,time_UTC,dates):
    days = date_to_days(dates)
    plt.subplot(3,1,1)
    plt.plot(days,latitude, "*")
    plt.title("Substorm data plotted with "+ str(len(latitude))+ " points")
    plt.ylabel("latitude")
    plt.xticks([])
    plt.subplot(3,1,2)
    plt.plot(days,mag_time, "*")
    plt.ylabel("time of day")
    plt.xticks([])
    plt.subplot(3,1,3)
    plt.plot(days,time_UTC, "*")
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
