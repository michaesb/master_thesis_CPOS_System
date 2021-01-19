import numpy as np
import matplotlib.pyplot as plt
import sys,time
from collections import Counter
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days

def create_bins(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)
    time_day_bins = np.zeros(N_event)
    hour_area = 4
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
                time_UTC_mag, magnetometer_values, gps_noise, time_gps):
    #NB shifted by another hour
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)*np.nan
    time_day_bins = np.zeros(N_event)*np.nan
    hour_area = 4
    events_collection = np.zeros((N_event,int(hour_area*60)))*np.nan
    event_gps_collection = np.zeros((N_event, 2*60*60*(hour_area+1)))*np.nan
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


                    gps_min_time = time_of_event[ii_bins] -(hour_area/2)
                    gps_max_time = time_of_event[ii_bins] +(hour_area/2)
                    bin_value = np.min(magnetometer_values[index_min:index_max])
                    if bin_value != bins[ii_bins-1]:
                        bins[ii_bins] = bin_value
                        #time of day value
                        time_day_bins[ii_bins] = days_magnetometer[i]+time_of_event[ii_bins]/24
                        # magnetotmeter values
                        events_collection[ii_bins,:] = magnetometer_values[index_min:index_max]
                        ###################### gps ######################
                        print("day:",days_magnetometer[i])
                        print("time of event",time_of_event[ii_bins])
                        if np.nansum(gps_noise[int(days_magnetometer[i]),:]) ==0:
                            print("empty day")
                            pass
                        elif gps_max_time>24 and gps_min_time <24:
                            print("Special condition nr 1")
                            print("gps_max_time",gps_max_time, "gps_min_time",gps_min_time)
                            if days_magnetometer[i] == 234.0 or days_magnetometer[i] == 235.0:
                                pass
                            else:
                                index_min_gps = np.where(gps_min_time < np.round(time_gps[int(days_magnetometer[i]),:],2))
                                print(time_gps[int(days_magnetometer[i]),:])
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(gps_max_time-24>np.round(time_gps[int(days_magnetometer[i])+1,:],2))
                                index_max_gps = int(index_max_gps[0][-1])
                                print("index_min_gps,index_max_gps",index_min_gps,index_max_gps)
                                print("time_check" ,time_gps[int(days_magnetometer[i]),index_min_gps],\
                                                time_gps[int(days_magnetometer[i]+1),index_max_gps]+24)
                                index_min_limit = len(gps_noise[int(days_magnetometer[i]),index_min_gps:])

                                print(index_min_limit, \
                                     len(event_gps_collection[ii_bins,0:index_min_limit]))

                                #filling the event_gps_collection with the first array
                                event_gps_collection[ii_bins,0:index_min_limit] = gps_noise[int(days_magnetometer[i]),index_min_gps:]
                                #filling the event_gps_collection with the second array
                                event_gps_collection[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                                gps_noise[int(days_magnetometer[i])+1,0:index_max_gps]
                        elif gps_min_time <0:
                            print("Special condition nr 2")
                            index_min_gps = np.where(24+gps_min_time < np.round(time_gps[int(days_magnetometer[i]-1),:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(gps_max_time < np.round(time_gps[int(days_magnetometer[i]),:],2))
                            print("preprocess",index_max_gps, "gps_max_time",gps_max_time,)
                            print(days_magnetometer[i],"which day, is fully nan",  np.nansum(gps_noise[int(days_magnetometer[i]),:]))
                            index_max_gps = int(index_max_gps[0][0])
                            index_min_limit = len(gps_noise[int(days_magnetometer[i]-1),index_min_gps:])
                            #filling the event_gps_collection with the first array
                            event_gps_collection[ii_bins,0:index_min_limit] = gps_noise[int(days_magnetometer[i]-1),index_min_gps:]

                            event_gps_collection[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                            gps_noise[int(days_magnetometer[i]),0:index_max_gps]
                        else:
                            print("----- \n regular")
                            print("gps_max_time",gps_max_time, "gps_min_time",gps_min_time)
                            index_min_gps = np.where(gps_min_time < np.round(time_gps[int(days_magnetometer[i]),:],2))
                            print("index_min preprocess",index_min_gps)
                            print(days_magnetometer[i],"which day")
                            print("number of nans",(np.sum(np.isnan(time_gps[int(days_magnetometer[i]),:]))))
                            if days_magnetometer[i] == 79.0:
                                print("-------------",days_magnetometer[i])
                                # print("time_gps ::80",  time_gps[int(days_magnetometer[i]),::100])
                                print(gps_min_time,gps_max_time)
                                pass
                            elif days_magnetometer[i] == 80.0:
                                print("---------------",days_magnetometer[i])
                                print(gps_min_time,gps_max_time)
                            else:
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(gps_max_time > np.round(time_gps[int(days_magnetometer[i]),:],2))
                                index_max_gps = int(index_max_gps[0][-1])
                                print(gps_min_time,gps_max_time,gps_max_time-gps_min_time, "time")
                                print(index_min_gps,index_max_gps,index_max_gps-index_min_gps, "index")
                                event_gps_collection[ii_bins,:(index_max_gps-index_min_gps)] = \
                                gps_noise[int(days_magnetometer[i]),index_min_gps:index_max_gps]
                    ii_bins+=1
                    print("beginning (end)")
    events_collection = events_collection[np.logical_not(np.isnan(bins)),:]
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_sorted = events_collection[indexing_sorted_bins,:]
    noise_gps_sorted = gps_noise[indexing_sorted_bins,:]
    return bins_sorted,time_day_bins, time_of_event, events_collection_sorted, noise_gps_sorted
