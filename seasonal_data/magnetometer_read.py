import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent

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

def date_to_days(dates,year=2018):
    """
    a date in 2018 in to the number of day in the year by using the numpy
    package datetime64
    """
    doy = np.zeros(len(dates))
    for i in range(len(dates)):
        doy[i] = (np.datetime64(dates[i]) - np.datetime64(str(year)+"-01-01"))\
                 /np.timedelta64(1,"D") + 1
    return doy


try:
    path = "/scratch/michaesb/20201025-17-57-supermag.csv"
    obj.read_csv(path)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/20201025-17-57-supermag.csv"
    obj.read_csv(path)
