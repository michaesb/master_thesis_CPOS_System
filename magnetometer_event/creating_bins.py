import numpy as np
import matplotlib.pyplot as plt
import sys,time
from collections import Counter
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days

def create_bins_gps_ROTI_mag(hour_area,dates_mag,dates_event, time_of_event, \
                             magnetometer_values, gps_noise, time_gps,
                             time_ROTI,ROTI_biint_TRO):
    #NB shifted forward by an hour
    #lenth of arrays
    show_individual_plot= False
    verbose = True
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
    events_collection_time_gps = np.zeros((N_event, 2*60*60*(hour_area+1)))*np.nan
    # counters in the for loops

    ii_bins = 0
    iii_gps = 0
    date = 0
    nr_storms = 0
    duplicate_avoided = 0
    missing_data_gps = 0
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
                        print(day+1, time_of_event[ii_bins])

                    if np.nansum(gps_noise[day,:]) == 0 or day==236 or day == 237:
                        missing_data_gps+= 1
                        bins[ii_bins] = np.nan
                        #time of day value
                        time_day_bins[ii_bins] = np.nan
                        ############# magnetotmeter values ################
                        events_collection_mag[ii_bins,:] = np.nan
                        ############# ROTI values #########################
                        events_collection_ROTI[ii_bins,:] = np.nan

                        if verbose:
                            print("empty day")
                        #continue
                    elif max_time>24:
                        """
                        if the day overlaps to the next day
                        """
                        if verbose:
                           print("Special condition nr 1")
                        try:
                            index_min_gps = np.where(min_time < np.round(time_gps[day,:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(max_time-24>np.round(time_gps[day+1,:],2))
                            index_max_gps = int(index_max_gps[0][-1])
                            index_border = len(gps_noise[day,index_min_gps:])
                            #filling the events_collection_gps with the first array
                            events_collection_gps[ii_bins,:index_border] = gps_noise[day,index_min_gps:]
                            events_collection_time_gps[ii_bins,0:index_border] = \
                            time_gps[day,index_min_gps:] -time_gps[day,index_min_gps]
                            #filling the events_collection_gps with the second array
                            events_collection_gps[ii_bins,index_border:index_border+index_max_gps] =\
                            gps_noise[day+1,:index_max_gps]
                            events_collection_time_gps[ii_bins,index_border:index_border+index_max_gps] =\
                            time_gps[day+1,:index_max_gps]+ 24-time_gps[day,index_min_gps]
                            nr_storms+=1
                        except IndexError:
                            missing_data_gps+=1
                            # plt.plot(time_gps[day,:], label= "first day" )
                            # plt.plot(time_gps[day+1,:],label="second day")
                            # plt.title(f"{day+1}")
                            # plt.legend()
                            # plt.show()
                            pass
                    elif min_time <0:
                        """
                        if the day overlaps to the previous day
                        """
                        if verbose:
                            print("Special condition nr 2")
                        try:
                            index_min_gps = np.where(24+min_time < np.round(time_gps[day-1,:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(max_time < np.round(time_gps[day,:],2))
                            index_max_gps = int(index_max_gps[0][0])
                            index_border = len(gps_noise[day-1,index_min_gps:])
                            #filling the events_collection_gps with the first array
                            events_collection_gps[ii_bins,0:index_border] = gps_noise[day-1,index_min_gps:]
                            events_collection_time_gps[ii_bins,0:index_border] = \
                            time_gps[day-1,index_min_gps:] -24-min_time
                            events_collection_gps[ii_bins,index_border:index_border+index_max_gps] =\
                            gps_noise[day,0:index_max_gps]
                            events_collection_time_gps[ii_bins,index_border:index_border+index_max_gps] =\
                            time_gps[day,0:index_max_gps] -min_time
                            nr_storms+=1
                        except IndexError:
                           # plt.plot(time_gps[day,:],label= "date of event")
                           # plt.plot(time_gps[day-1,:],label="previous day")
                           # plt.legend()
                           # plt.title(f"{day+1}")
                           # plt.show()
                           missing_data_gps += 1
                           pass

                    else:
                        if verbose:
                            print("regular condition")
                        try:
                            index_min_gps = np.where(min_time < np.round(time_gps[day,:],2))
                            index_min_gps = int(index_min_gps[0][0])
                            index_max_gps = np.where(max_time > np.round(time_gps[day,:],2))
                            index_max_gps = int(index_max_gps[0][-1])
                            events_collection_gps[ii_bins,:(index_max_gps - index_min_gps)] = \
                            gps_noise[day,index_min_gps:index_max_gps]
                            events_collection_time_gps[ii_bins,:(index_max_gps - index_min_gps)] = \
                            time_gps[day,index_min_gps:index_max_gps]-min_time
                            nr_storms+=1
                        except IndexError:
                           # plt.plot(time_gps[day,:], label= "first day" )
                           # plt.title(f"{day+1}")
                           # plt.show()
                           missing_data_gps+=1
                           pass
                    if verbose:
                        print("min",min_time, time_gps[day,index_min_gps])
                        print("max",max_time,time_gps[day,index_max_gps])

                    if show_individual_plot:
                        fig,ax = plt.subplots(3,1)
                        ax[0].plot(events_collection_mag[ii_bins,:])
                        ax[0].plot(np.ones_like(events_collection_mag[ii_bins,:])*250,"g",linewidth=0.5)
                        ax[0].plot(np.ones_like(events_collection_mag[ii_bins,:])*400,"g",linewidth=0.5)
                        ax[0].set_ylabel("Magnetic North [nT]")
                        ax[0].set_title(f"day {day+1} magnetometer values with substorm trigger, \n ROTI values and \n noise from gps at Tromsø in 2018")
                        ax[0].set_ylim(-500,400)
                        ax[0].grid("on")

                        ax[1].plot(events_collection_ROTI[ii_bins,:],".-")
                        ax[1].set_ylabel("ROTI [TEC/min]")
                        ax[1].set_ylim(0,10)
                        ax[1].grid("on")

                        ax[2].plot(events_collection_time_gps[ii_bins,:],events_collection_gps[ii_bins,:],".")
                        ax[2].set_yscale("log")
                        ax[2].set_ylim(1e-4, 1e-1)
                        ax[2].set_ylabel("GPS noise")
                        ax[2].set_xlabel("days")
                        ax[2].grid("on")
                        plt.show()
                else:
                    duplicate_avoided += 1
                ii_bins+=1

    events_collection_mag = events_collection_mag[np.logical_not(np.isnan(bins)),:]
    events_collection_ROTI = events_collection_ROTI[np.logical_not(np.isnan(bins)),:]
    events_collection_gps = events_collection_gps[np.logical_not(np.isnan(bins)),:]
    events_collection_time_gps = events_collection_time_gps[np.logical_not(np.isnan(bins)),:]
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)
    #sorting events after minimum mag value
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_mag_sorted = events_collection_mag[indexing_sorted_bins,:]
    ROTI_event_sorted = events_collection_ROTI[indexing_sorted_bins,:]
    noise_gps_sorted = events_collection_gps[indexing_sorted_bins,:]
    time_gps_sorted = events_collection_time_gps[indexing_sorted_bins,:]
    if verbose:
        print(f"nr_storms {nr_storms} N_event {N_event} duplicate substorms avoided {duplicate_avoided} \n",
              f"missing data prevented collection of gps_data {missing_data_gps}")
    return bins_sorted,time_day_bins, time_of_event, events_collection_mag_sorted,\
           ROTI_event_sorted, noise_gps_sorted, time_gps_sorted, N_event-duplicate_avoided,N_event-missing_data_gps-duplicate_avoided
