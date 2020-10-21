import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent

obj = ReadSubstormEvent()

try:
    path = "/scratch/michaesb/substorm_event_list_2018.csv"
    obj.read_csv(path)

except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/substorm_event_list_2018.csv"
    obj.read_csv(path)

N = obj.datapoints
lat = obj.latitude
mag_time = obj.magnetic_time
date_UTC, year = obj.day_of_year
print("year",year," datapoints", N, "\n")
print("lat",lat[:10])
print("magnetic_time",mag_time[:10])
print("date",date_UTC[:10])
def filtering_to_Norway_night(latitude, magnetic_time,date_UTC,N,verbose=False):
    ind_arr = np.ones(len(latitude))
    ind_arr = np.where(58 > latitude ,np.nan,ind_arr)
    ind_arr = np.where(latitude > 71,np.nan,ind_arr)
    ind_arr = np.where(23 < magnetic_time,np.nan,ind_arr)
    ind_arr = np.where(magnetic_time < 1,np.nan,ind_arr)
    latitude =latitude[np.logical_not(np.isnan(ind_arr))]
    magnetic_time =magnetic_time[np.logical_not(np.isnan(ind_arr))]
    date_UTC =date_UTC[np.logical_not(np.isnan(ind_arr))]
    if verbose:
        print("reduced from ",N, " to ", len(date_UTC), "ratio:", len(date_UTC))
    return latitude, magnetic_time, date_UTC
latitude, mag_time, date_UTC = filtering_to_Norway_night(lat,mag_time,date_UTC,N,verbose=True)

print("lat",lat[:10])
print("magnetic_time",mag_time[:10])
print("date",date_UTC[:10])
