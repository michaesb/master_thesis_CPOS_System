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
                time_UTC_mag, magnetometer_values, gps_noise, time_gps,
                time_ROTI,ROTI_biint_TRO):
    #NB shifted forward by an hour
    #lenth of arrays
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    #conversion of days
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)

    # creating empy arrays to be filled ############
    #bins
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)*np.nan
    time_day_bins = np.zeros(N_event)*np.nan

    #events_collection
    hour_area = 4
    events_collection_mag = np.zeros((N_event,int(hour_area*60)))*np.nan
    events_collection_ROTI = np.zeros((N_event,int(hour_area)))*np.nan
    events_collection_gps = np.zeros((N_event, 2*60*60*(hour_area+1)))*np.nan

    # counters in the for loops
    ii_bins = 0
    iii_gps = 0
    date = 0
    nr_storms = 0
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
                        events_collection_mag[ii_bins,:] = magnetometer_values[index_min:index_max]
                        ###################### gps ######################
                        print("--------")
                        print("day:",days_magnetometer[i]-1)
                        print("time of event",time_of_event[ii_bins])
                        # print("min",gps_min_time, time_gps[int(days_magnetometer[i]),index_min_gps] )
                        # print("max",gps_max_time, time_gps[int(days_magnetometer[i]),index_max_gps] )
                        if np.nansum(gps_noise[int(days_magnetometer[i])-1,:]) ==0:
                            print("empty day")
                            pass
                        elif gps_max_time>24 and gps_min_time <24:
                            print("Special condition nr 1")
                            if days_magnetometer[i] == 234.0 or\
                               days_magnetometer[i] == 237.0 or days_magnetometer[i] == 55:
                                pass
                            else:
                                nr_storms+=1
                                print(time_gps[int(days_magnetometer[i])-1,:])
                                index_min_gps = np.where(gps_min_time < np.round(time_gps[int(days_magnetometer[i]-1),:],2))
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(gps_max_time-24>np.round(time_gps[int(days_magnetometer[i]-1)+1,:],2))
                                try:
                                    index_max_gps = int(index_max_gps[0][-1])
                                except:
                                    plt.plot(time_gps[int(days_magnetometer[i]),:],gps_noise[int(days_magnetometer[i]),:])
                                    plt.show()
                                index_min_limit = len(gps_noise[int(days_magnetometer[i]-1),index_min_gps:])
                                #filling the events_collection_gps with the first array
                                events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[int(days_magnetometer[i]-1),index_min_gps:]
                                #filling the events_collection_gps with the second array
                                events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                                gps_noise[int(days_magnetometer[i]-1)+1,0:index_max_gps]
                        elif gps_min_time <0:
                            print("Special condition nr 2")
                            if days_magnetometer[i] == 238.0:
                                print("passing over day 237")
                                continue
                            nr_storms += 1
                            index_min_gps = np.where(24+gps_min_time < np.round(time_gps[int(days_magnetometer[i]-2),:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(gps_max_time < np.round(time_gps[int(days_magnetometer[i]-1),:],2))
                            index_max_gps = int(index_max_gps[0][0])
                            index_min_limit = len(gps_noise[int(days_magnetometer[i]-2),index_min_gps:])
                            #filling the events_collection_gps with the first array
                            events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[int(days_magnetometer[i]-2),index_min_gps:]

                            events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                            gps_noise[int(days_magnetometer[i]-1),0:index_max_gps]
                        else:
                            print("regular condition")
                            nr_storms+=1
                            index_min_gps = np.where(gps_min_time < np.round(time_gps[int(days_magnetometer[i]-1),:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(gps_max_time > np.round(time_gps[int(days_magnetometer[i]-1),:],2))
                            index_max_gps = int(index_max_gps[0][-1])
                            events_collection_gps[ii_bins,:(index_max_gps-index_min_gps)] = \
                            gps_noise[int(days_magnetometer[i]-1),index_min_gps:index_max_gps]
                        print("min",gps_min_time, time_gps[int(days_magnetometer[i]-1),index_min_gps])
                        print("max",gps_max_time,time_gps[int(days_magnetometer[i]-1),index_max_gps])
                        # plt.plot(events_collection_gps[ii_bins,:])
                        # plt.title("day:"+str(days_magnetometer[i]))
                        # plt.yscale("log")
                        # plt.show()
                    ii_bins+=1

    events_collection_mag = events_collection_mag[np.logical_not(np.isnan(bins)),:]
    events_collection_gps = events_collection_gps[np.logical_not(np.isnan(bins)),:]
    events_collection_ROTI = events_collection_ROTI[np.logical_not(np.isnan(bins)),:]
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)

    #sorting events after minimum mag value
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_mag_sorted = events_collection_mag[indexing_sorted_bins,:]
    ROTI_event_sorted = events_collection_ROTI[indexing_sorted_bins,:]
    noise_gps_sorted = events_collection_gps[indexing_sorted_bins,:]
    print("nr_storms", nr_storms, "N_event",N_event)
    return bins_sorted,time_day_bins, time_of_event, events_collection_mag_sorted,\
           ROTI_event_sorted, noise_gps_sorted
