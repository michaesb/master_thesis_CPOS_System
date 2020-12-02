import numpy as np
import time
def filtering_to_Norway_night(latitude, magnetic_time,time_UTC,dates,verbose=False):
    N = len(latitude)
    evening_time = 20
    morning_time = 4
    ind_arr = np.ones(len(latitude))
    #filtering out magnetic time that is not in the night
    ind_arr_1 = np.where(evening_time > magnetic_time,0, ind_arr)
    ind_arr_2 = np.where(morning_time < magnetic_time,0,ind_arr)
    ind_arr = np.where(ind_arr_1 +ind_arr_2 != 0, 1, np.nan)

    #filtering out the day UTC time
    ind_arr_3 = np.where(evening_time > time_UTC, 0,ind_arr)
    ind_arr_4 = np.where(morning_time < time_UTC, 0, ind_arr)
    ind_arr = np.where(ind_arr_3 +ind_arr_4 != 0, 1, np.nan)
    print(np.nansum(ind_arr))
    # filtering latitude that is not in Norway
    ind_arr = np.where(58 > latitude ,np.nan,ind_arr)
    ind_arr = np.where(latitude > 71,np.nan,ind_arr)
    latitude =latitude[np.logical_not(np.isnan(ind_arr))]
    magnetic_time =magnetic_time[np.logical_not(np.isnan(ind_arr))]
    time_UTC =time_UTC[np.logical_not(np.isnan(ind_arr))]
    dates = dates[np.logical_not(np.isnan(ind_arr))]
    if verbose:
        print("reduced from ",N, " to ", len(time_UTC), \
              "ratio:", 100*len(time_UTC)/N, " %")
    return latitude, magnetic_time, time_UTC, dates
