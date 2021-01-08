import numpy as np
import sys,time
from collections import Counter
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days

def create_bins(dates_mag,dates_event, time_of_event, \
                time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)
    time_day_bins = np.zeros(N_event)
    hour_area = 3
    events_collection = np.zeros((N_event,int(hour_area*60)))*np.nan
    j=0
    date = 0
    for i in range(N_mag):
        if days_magnetometer[i] in days_event:
            if date != days_magnetometer[i]:
                date = days_magnetometer[i]
                for k in range(Counter(days_event)[days_magnetometer[i]]):
                    index_min, index_max = i+int((time_of_event[j] - (hour_area/2))*60)\
                                          ,i+int((time_of_event[j] + (hour_area/2))*60)
                    if index_max-index_min != hour_area*60:
                        index_min+=index_max-index_min-hour_area*60

                    bin_value = np.min(magnetometer_values[index_min:index_max])
                    if bin_value != bins[j-1]:
                        bins[j] = bin_value
                        events_collection[j,:] = magnetometer_values[index_min:index_max]
                        time_day_bins[j] = days_magnetometer[i]+time_of_event[j]/24
                    else:
                        bins[j] = np.nan
                        time_day_bins[j] = np.nan
                    j+=1
    events_collection = events_collection[np.logical_not(np.isnan(bins)),:]
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_sorted = events_collection[indexing_sorted_bins,:]
    return bins_sorted,time_day_bins, time_of_event, events_collection_sorted


def create_bins_with_noise_sort(dates_mag,dates_event, time_of_event, \
                time_UTC_mag, magnetometer_values, gps_noise):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)*np.nan
    time_day_bins = np.zeros(N_event)*np.nan
    hour_area = 3
    events_collection = np.zeros((N_event,int(hour_area*60)))*np.nan
    event_gps_collection = np.zeros((N_event, int(hour_area*3600)))*np.nan
    ii_bins=0
    iii_gps =0
    date = 0
    for i in range(N_mag):

        if days_magnetometer[i] in days_event:
            if date != days_magnetometer[i]:
                date = days_magnetometer[i]
                for k in range(Counter(days_event)[days_magnetometer[i]]):
                    index_min, index_max = i+int((time_of_event[ii_bins] - (hour_area/2))*60)\
                                          ,i+int((time_of_event[ii_bins] + (hour_area/2))*60)
                    if index_max-index_min != hour_area*60:
                        index_min+=index_max-index_min-hour_area*60

                    bin_value = np.min(magnetometer_values[index_min:index_max])
                    if bin_value != bins[ii_bins-1]:
                        bins[ii_bins] = bin_value
                        events_collection[ii_bins,:] = magnetometer_values[index_min:index_max]
                        time_day_bins[ii_bins] = days_magnetometer[i]+time_of_event[ii_bins]/24

                    ii_bins+=1
        iii_gps += 60
    events_collection = events_collection[np.logical_not(np.isnan(bins)),:]
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_sorted = events_collection[indexing_sorted_bins,:]
    noise_gps_sorted = 1
    return bins_sorted,time_day_bins, time_of_event, events_collection_sorted, noise_gps_sorted
