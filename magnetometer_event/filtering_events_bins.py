import numpy as np
import matplotlib.pyplot as plt
import sys, time
from collections import Counter
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

def create_bins(dates_mag,dates_event, time_of_event, time_UTC_mag, magnetometer_values):
    N_mag = len(dates_mag)
    N_event = len(dates_event)
    days_event = date_to_days(dates_event)
    days_magnetometer = date_to_days(dates_mag)
    time_stamp_event = np.zeros(N_mag)*np.nan
    bins = np.zeros(N_event)
    time_day_bins = np.zeros(N_event)
    hour_area = 2
    events_collection = np.zeros((N_event,int(hour_area*60)))*np.nan
    print(np.shape(events_collection))
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
    bins = bins[np.logical_not(np.isnan(bins))]
    indexing_sorted_bins = np.argsort(bins)
    bins_sorted = bins[indexing_sorted_bins]
    events_collection_sorted = events_collection[indexing_sorted_bins,:]
    print(bins_sorted)
    return bins_sorted,time_day_bins, time_of_event, events_collection_sorted


def plot_histograms(bins_sorted,time_day_bins, time_of_event):
    borders = [bins_sorted[int((len(bins_sorted)-1)/3)],bins_sorted[int((len(bins_sorted)-1)*2/3)]]
    print(bins_sorted)
    print("length of bins", len(bins_sorted))
    print("size of each bin",len(bins_sorted)/3)

    plt.hist(bins_sorted, bins = 30)
    plt.axvline(x=borders[0],color ="r")
    plt.axvline(x=borders[1],color ="r")
    plt.title("2018, Tromso,\n Max magnetometer value of a substorm event. \n"+\
              "Red lines are the lines for the borders which is " +str(borders[0])\
              +" and " +str(borders[1])+ " nT")
    plt.xlabel("minimum of the north component magnetometer [nT]")
    plt.ylabel("number of occurances")
    plt.show()
    plt.hist(time_day_bins, bins = 30)
    plt.title("Time of year when the substorm occurs")
    plt.xlabel("day of year")
    plt.ylabel("number of occurances")
    plt.show()
    plotting_bins_array = np.concatenate([time_of_event[time_of_event>16]-20,time_of_event[time_of_event<16]+4])
    plt.hist(plotting_bins_array,color = "b", bins = 80)
    plt.title("Distrubution of what time the substorm occurs")
    plt.xlabel("time of day [UT+1]")
    plt.xticks(range(9),labels=[str(20),str(21),str(22),str(23),str(24),\
                                str(1),str(2),str(3),str(4)])
    plt.show()

def plot_all_events(events_collection):
    index_third, index_two_thirds = int(len(events_collection)/3),\
                                    int(len(events_collection)*2/3)
    for i in range(len(events_collection)):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection, axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("All recorded substorms by the magnetometer in Tromso in 2018")
    plt.xlabel("minutes")
    plt.ylabel("B-value [nT]")
    plt.legend()
    plt.show()
    for i in range(index_third):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[:index_third], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("First bin of recorded substorms by the magnetometer in Tromso in 2018")
    plt.xlabel("minutes")
    plt.ylabel("B-value [nT] (Smaller than -258.9 nT)")
    plt.legend()
    plt.show()
    for i in range(index_third,index_two_thirds ):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[index_third:index_two_thirds], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("Second bin of substorms by the magnetometer in Tromso in 2018")
    plt.xlabel("minutes")
    plt.ylabel("B-value [nT] (between -258.9 nT and -441.9 nT)")
    plt.legend()
    plt.show()
    for i in range(index_two_thirds, len(events_collection)):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[index_two_thirds:], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("Third bin of substorms by the magnetometer in Tromso in 2018")
    plt.xlabel("minutes")
    plt.ylabel("B-value [nT] (substorms above -441.9 nT)")
    plt.legend()
    plt.show()





obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()

try:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/HDD Linux/data/"
    path_event = desktop_path+"/substorm_event_list_2018.csv"
    path_mag = desktop_path+"/20201025-17-57-supermag.csv"
    print("substorm event reader")
    obj_event.read_csv(path_event,verbose = False)
    print("magnetometer reader")
    obj_mag.read_csv(path_mag, verbose = False)


#magnetometer reader
dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("TRO")

#then event reader
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

bins_sorted,time_day_bins, time_of_event,events_collection = \
create_bins(dates_mag,dates_event, Norway_time,time_UTC_mag ,magnetic_north)

plot_histograms(bins_sorted,time_day_bins, time_of_event)

plot_all_events(events_collection)
