import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository

from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent


path = "/scratch/michaesb/substorm_event_list_2018.csv"
obj = ReadSubstormEvent()
obj.read_csv(path)
obj.
def filtering_to_Norway_night(latitude, magnetic_time,date):
    indexing_array = np.ones(len(latitude))
    indexing_array = np.where(58 < latitude <71,np.nan,indexing_array)
    indexing_array = np.where(19> magnetic_time <24,np.nan,indexing_array)
    indexing_array = np.where(magnetic_time <7,np.nan,indexing_array)
    indexing_array = np.where(19> magnetic_time <24,np.nan,indexing_array)
    X_filtered = X
    return latitude, magnetic_time,date
