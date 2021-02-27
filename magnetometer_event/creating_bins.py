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

                    index_min_mag, index_max_mag = i+int((time_of_event[j] - (hour_area/2))*60)\
                                          ,i+int((time_of_event[j] + (hour_area/2))*60)
                    if index_max_mag-index_min_mag != hour_area*60:
                        index_min_mag+=index_max_mag-index_min_mag-hour_area*60
                    bin_value = np.min(magnetometer_values[index_min_mag:index_max_mag])

                    if bin_value != bins[j-1]:
                        bins[j] = bin_value
                        events_collection[j,:] = magnetometer_values[index_min_mag:index_max_mag]
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
    verbose = False
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
    events_collection_ROTI = np.zeros((N_event,int(hour_area*12)))*np.nan
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
                    #finding the minimum and max time for the area of the event
                    min_time = time_of_event[ii_bins] - (hour_area/2)
                    max_time = time_of_event[ii_bins] + (hour_area/2)

                    #finding indexes for the magnetometer
                    index_min_mag, index_max_mag = i+int((time_of_event[ii_bins] - (hour_area/2))*60)\
                                                  ,i+int((time_of_event[ii_bins] + (hour_area/2))*60)


                    if index_max_mag-index_min_mag != hour_area*60:
                        index_min_mag+=index_max_mag-index_min_mag-hour_area*60



                    #finding indexing for the ROTI
                    index_min_ROTI, index_max_ROTI = int(i/5 + min_time*12) \
                                                    ,int(i/5 + max_time*12)

                    # print(i/5 + min_time*12, i/5 + max_time*12)
                    # print(index_max_ROTI-index_min_ROTI,int(i/5 + min_time*12) - int(i/5 + max_time*12))
                    if index_max_ROTI-index_min_ROTI != hour_area*12:
                        index_min_ROTI+=index_max_ROTI-index_min_ROTI-hour_area*12


                    bin_value = np.min(magnetometer_values[index_min_mag:index_max_mag])
                    print("hello",Counter(days_event)[days_magnetometer[i]],k,i/24/60)

                    if bin_value != bins[ii_bins-1]:

                        bins[ii_bins] = bin_value
                        #time of day value
                        time_day_bins[ii_bins] = days_magnetometer[i]+time_of_event[ii_bins]/24
                        ############# magnetotmeter values ################
                        events_collection_mag[ii_bins,:] = magnetometer_values[index_min_mag:index_max_mag]
                        ############# ROTI values #########################
                        events_collection_ROTI[ii_bins,:] = ROTI_biint_TRO[index_min_ROTI:index_max_ROTI]

                        ###################### gps ######################
                        if verbose:
                            print("--------")
                            print(index_min_ROTI,index_max_ROTI)
                        print("---------------------------")
                        print("day:",days_magnetometer[i],"time of event",time_of_event[ii_bins])
                        print("min_time",min_time*12,"max time",max_time *12)
                        print((time_ROTI[index_min_ROTI]-days_magnetometer[i])*24*12 , \
                           (time_ROTI[index_max_ROTI]-days_magnetometer[i])*24*12)
                            # time.sleep(5)
                            # print("min",min_time, time_gps[int(days_magnetometer[i]),index_min_gps] )
                            # print("max",max_time, time_gps[int(days_magnetometer[i]),index_max_gps] )
                        if np.nansum(gps_noise[int(days_magnetometer[i])-1,:]) == 0:
                            if verbose:
                                print("empty day")
                            pass
                        elif max_time>24 and min_time <24:
                            if verbose:
                                print("Special condition nr 1")
                            try:
                                index_min_gps = np.where(min_time < np.round(time_gps[day,:],2))
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(max_time-24>np.round(time_gps[day+1,:],2))
                            except:
                                print(time_gps[int(days_magnetometer[i])-1,:])
                                print(time_gps[int(days_magnetometer[i]),:])
                            try:
                                index_max_gps = int(index_max_gps[0][-1])
                                index_min_limit = len(gps_noise[day,index_min_gps:])
                                #filling the events_collection_gps with the first array
                                events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[day,index_min_gps:]
                                #filling the events_collection_gps with the second array
                                events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                                gps_noise[day+1,0:index_max_gps]
                            except:
                                pass
                        elif min_time <0:
                            if verbose:
                                print("Special condition nr 2")
                            if days_magnetometer[i] == 238.0:
                                if verbose:
                                    print("passing over day 237")
                            else:
                                nr_storms += 1
                                index_min_gps = np.where(24+min_time < np.round(time_gps[int(days_magnetometer[i]-2),:],2))
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(max_time < np.round(time_gps[int(days_magnetometer[i])-1,:],2))
                                index_max_gps = int(index_max_gps[0][0])
                                index_min_limit = len(gps_noise[int(days_magnetometer[i]-2),index_min_gps:])
                                #filling the events_collection_gps with the first array
                                events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[int(days_magnetometer[i]-2),index_min_gps:]

                                events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                                gps_noise[int(days_magnetometer[i])-1,0:index_max_gps]
                        else:
                            if verbose:
                                print("regular condition")
                                # plt.plot(time_gps[day,:])
                                # plt.title(str(days_magnetometer[i]))
                                # plt.show()
                            if days_magnetometer[i] ==238:
                                pass
                            else:
                                nr_storms+=1
                                index_min_gps = np.where(min_time < np.round(time_gps[int(days_magnetometer[i]),:],2))
                                index_min_gps = int(index_min_gps[0][0])
                                index_max_gps = np.where(max_time > np.round(time_gps[int(days_magnetometer[i]),:],2))
                                index_max_gps = int(index_max_gps[0][-1])
                                events_collection_gps[ii_bins,:(index_max_gps - index_min_gps)] = \
                                gps_noise[int(days_magnetometer[i]),index_min_gps:index_max_gps]
                        if verbose:
                            print("min",min_time, time_gps[int(days_magnetometer[i]),index_min_gps])
                            print("max",max_time,time_gps[int(days_magnetometer[i]),index_max_gps])
                        # plt.plot(events_collection_gps[ii_bins,:])
                        # plt.title("days_magnetometer[i]:"+str(days_magnetometer[i]))
                        # plt.yscale("log")
                        # plt.show()
                    ii_bins+=1
                    # if ii_bins ==10:
                    #     # break
                    #     exit()
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

def create_bins_gps_ROTI_mag(hour_area,dates_mag,dates_event, time_of_event, \
                time_UTC_mag, magnetometer_values, gps_noise, time_gps,
                time_ROTI,ROTI_biint_TRO):
    #NB shifted forward by an hour
    #lenth of arrays
    verbose = False
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
    events_collection_mag = np.zeros((N_event,int(hour_area*60)))*np.nan
    events_collection_ROTI = np.zeros((N_event,int(hour_area*12)))*np.nan
    events_collection_gps = np.zeros((N_event, 2*60*60*(hour_area+1)))*np.nan

    # counters in the for loops

    ii_bins = 0
    iii_gps = 0
    date = 0
    nr_storms = 0
    for day in range(365):
        if day+1 in days_event:
            for k in range(Counter(days_event)[day+1]):
                #finding the minimum and max time for the area of the event
                min_time = time_of_event[ii_bins] - (hour_area/2)
                max_time = time_of_event[ii_bins] + (hour_area/2)

                #finding indexes for the magnetometer
                index_min_mag, index_max_mag = int(day*24*60+(min_time)*60)\
                                              ,int(day*24*60+(max_time)*60)

                if index_max_mag-index_min_mag != hour_area*60:
                    index_min_mag+=index_max_mag-index_min_mag-hour_area*60

                #finding indexing for the ROTI
                index_min_ROTI, index_max_ROTI = int(day*24*12 + min_time*12) \
                                                ,int(day*24*12 + max_time*12)

                if index_max_ROTI-index_min_ROTI != hour_area*12:
                    index_min_ROTI+=index_max_ROTI-index_min_ROTI-hour_area*12


                bin_value = np.min(magnetometer_values[index_min_mag:index_max_mag])

                if bin_value != bins[ii_bins-1]:

                    bins[ii_bins] = bin_value
                    #time of day value
                    time_day_bins[ii_bins] = day+time_of_event[ii_bins]/24
                    ############# magnetotmeter values ################
                    events_collection_mag[ii_bins,:] = magnetometer_values[index_min_mag:index_max_mag]
                    ############# ROTI values #########################
                    events_collection_ROTI[ii_bins,:] = ROTI_biint_TRO[index_min_ROTI:index_max_ROTI]
                    ###################### gps ######################
                    if verbose:
                        print("--------")
                    print("-----------------------")
                    print(day+1, time_of_event[ii_bins])
                    print(min_time,max_time)
                    print(index_min_ROTI,index_max_ROTI)
                    print(min_time*12,max_time*12)
                    print((time_ROTI[index_min_ROTI]-day)*24,(time_ROTI[index_max_ROTI]-day)*24 )
                    # plt.plot(time_ROTI)
                    # plt.plot(time_ROTI[:index_min_ROTI])
                    # plt.show()
                         # time.sleep(5)
                    if np.nansum(gps_noise[day,:]) == 0:
                        if verbose:
                            print("empty day")
                        pass
                    #elif max_time>24 and min_time <24:
                    #    if verbose:
                    #         print("Special condition nr 1")
                    #     try:
                    #         index_min_gps = np.where(min_time < np.round(time_gps[day,:],2))
                    #         index_min_gps = int(index_min_gps[0][0])
                    #         index_max_gps = np.where(max_time-24>np.round(time_gps[day+1,:],2))
                    #     except:
                    #         print(time_gps[day,:])
                    #         print(time_gps[day+1,:])
                    #     try:
                    #         index_max_gps = int(index_max_gps[0][-1])
                    #         index_min_limit = len(gps_noise[day,index_min_gps:])
                    #         #filling the events_collection_gps with the first array
                    #         events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[day,index_min_gps:]
                    #         #filling the events_collection_gps with the second array
                    #         events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                    #         gps_noise[day+1,0:index_max_gps]
                    #     except:
                    #         pass
                    # elif min_time <0:
                    #     if verbose:
                    #         print("Special condition nr 2")
                    #     else:
                    #         nr_storms += 1
                    #         index_min_gps = np.where(24+min_time < np.round(time_gps[day-1,:],2))
                    #         index_min_gps = int(index_min_gps[0][0])
                    #         index_max_gps = np.where(max_time < np.round(time_gps[day,:],2))
                    #         index_max_gps = int(index_max_gps[0][0])
                    #         index_min_limit = len(gps_noise[day-1,index_min_gps:])
                    #         #filling the events_collection_gps with the first array
                    #         events_collection_gps[ii_bins,0:index_min_limit] = gps_noise[day-1,index_min_gps:]
                    #
                    #         events_collection_gps[ii_bins,index_min_limit:index_min_limit+index_max_gps] =\
                    #         gps_noise[day,0:index_max_gps]
                    # else:
                    #     if verbose:
                    #         print("regular condition")
                    #         # plt.plot(time_gps[day,:])
                    #         # plt.title(str(days_magnetometer[i]))
                    #         # plt.show()
                    #     else:
                    #         nr_storms+=1
                    #         index_min_gps = np.where(min_time < np.round(time_gps[day,:],2))
                    #         index_min_gps = int(index_min_gps[0][0])
                    #         index_max_gps = np.where(max_time > np.round(time_gps[day,:],2))
                    #         index_max_gps = int(index_max_gps[0][-1])
                    #         events_collection_gps[ii_bins,:(index_max_gps - index_min_gps)] = \
                    #         gps_noise[day,index_min_gps:index_max_gps]
                    # if verbose:
                    #     print("min",min_time, time_gps[day,index_min_gps])
                    #     print("max",max_time,time_gps[day,index_max_gps])
                    # plt.plot(events_collection_gps[ii_bins,:])
                    # plt.title("day:"+str(days_magnetometer[i]))
                    # plt.yscale("log")
                    # plt.show()
                ii_bins+=1
                # if ii_bins ==10:
                #      # break
                #      exit()
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
