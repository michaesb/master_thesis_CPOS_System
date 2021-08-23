import numpy as np
import matplotlib.pyplot as plt
import sys, time

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from magnetometer_event.filtering_events import filtering_to_Norway_night


def plot_latitude_time(latitude, mag_time, time_UTC, dates):
    days = date_to_days(dates)
    print(days)
    plt.subplot(3, 1, 1)
    plt.plot(days, latitude, "*")
    plt.title("Substorm data plotted with " + str(len(latitude)) + " points")
    plt.ylabel("latitude")
    plt.xticks([])
    plt.subplot(3, 1, 2)
    plt.plot(days, mag_time, "*")
    plt.ylabel("time of day")
    plt.xticks([])
    plt.subplot(3, 1, 3)
    plt.plot(days, time_UTC, "*")
    plt.ylabel("time of day")
    plt.xlabel("day of year")
    plt.show()


obj = ReadSubstormEvent()

try:
    path = "/scratch/michaesb/substorm_event_list_2018.csv"
    obj.read_csv(path)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/substorm_event_list_2018.csv"
    obj.read_csv(path)

evening_time = 20
morning_time = 4

N = obj.datapoints
lat = obj.latitude
mag_time = obj.magnetic_time
time_UTC = obj.dates_time
date_UTC, year = obj.day_of_year

Norway_time = time_UTC + 1
plot_latitude_time(lat, mag_time, Norway_time, date_UTC)
lat, mag_time, Norway_time, dates = filtering_to_Norway_night(
    lat, mag_time, Norway_time, date_UTC, N, verbose=True
)
plot_latitude_time(lat, mag_time, Norway_time, dates)
