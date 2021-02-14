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
from magnetometer_event.creating_bins import create_bins

def plot_histograms(bins_sorted, time_day_bins, time_of_event):
    borders = [bins_sorted[int((len(bins_sorted)-1)/3)],bins_sorted[int((len(bins_sorted)-1)*2/3)]]

    index_third, index_two_thirds = int(len(bins_sorted)/3),\
                                    int(len(bins_sorted)*2/3)

    plt.hist(bins_sorted, bins = 30)
    plt.axvline(x=borders[0], color ="r")
    plt.axvline(x=borders[1], color ="r")
    plt.title("2018, "+station+",\n Max magnetometer value of a substorm event. \n"+\
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

def plot_all_events(events_collection,bins_sorted):
    borders = [bins_sorted[int((len(bins_sorted)-1)/3)],bins_sorted[int((len(bins_sorted)-1)*2/3)]]

    index_third, index_two_thirds = int(len(events_collection)/3),\
                                    int(len(events_collection)*2/3)
    hour_area = 4
    nr_of_xticks = hour_area*2+1
    time = np.linspace(-(hour_area/2 -1)*60,(hour_area/2+1)*60,nr_of_xticks)
    for i in range(len(events_collection)):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection, axis = 0)
    nfive_percentile = np.percentile(events_collection,95, axis =0)
    five_percentile = np.percentile(events_collection,5, axis =0)
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95 % percentile")
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5 % percentile")
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("All recorded substorms by the magnetometer in "+station+" in 2018")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT]")
    plt.xticks(np.linspace(0,len(events_collection)*0.666,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection))

    plt.legend()
    plt.show()

    for i in range(index_two_thirds, len(events_collection)):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[index_two_thirds:], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("Third bin of substorms by the magnetometer in "+station+" in 2018")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT] (smaller than "+str(borders[1])+" nT)")
    plt.xticks(np.linspace(0,len(events_collection)*0.666,nr_of_xticks),time)
    plt.legend()
    plt.ylim(-700,np.max(events_collection))
    plt.show()

    for i in range(index_third,index_two_thirds):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[index_third:index_two_thirds], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("Second bin of substorms by the magnetometer in "+station+" in 2018")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT] (between "+str(borders[0])+"nT and "+str(borders[1])+" nT)")
    plt.xticks(np.linspace(0,len(events_collection)*0.666,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection))
    plt.legend()
    plt.show()

    for i in range(index_third):
        plt.plot(events_collection[i,:], linewidth = 0.5)
    average_event = np.nanmedian(events_collection[:index_third], axis = 0)
    plt.plot(average_event, linewidth = 3, color = "black", label="median value")
    plt.title("First bin of recorded substorms by the magnetometer in "+station+" in 2018")
    plt.ylabel("North component B-value [nT] (bigger than "+str(borders[0])+" nT)")
    plt.xlabel("minutes")
    plt.xticks(np.linspace(0,len(events_collection)*0.666,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection))
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
    desktop_path = "/run/media/michaelsb/data_ssd/data/"
    path_event = desktop_path+"/substorm_event_list_2018.csv"
    path_mag = desktop_path+"/20201025-17-57-supermag.csv"
    print("substorm event reader")
    obj_event.read_csv(path_event,verbose = False)
    print("substorm done")
    print("magnetometer reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer done")


#magnetometer reader
try:
    station = sys.argv[1]
except IndexError:
    station = "TRO"

dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data(station)
stations_dictionary_GEO_coord = {"KIL":[69.02, 20.79],"TRO":[69.66, 18.94],\
                                 "ABK":[68.35, 18.82],"AND":[69.30, 16.03],\
                                 "DOB":[62.07,  9.11],"DON":[66.11, 12.50],\
                                 "JCK":[66.40, 16.98],"KAR":[59.21,  5.24],\
                                 "MAS":[69.46, 23.70],"NOR":[71.09, 25.79],\
                                 "RVK":[64.94, 10.99],"SOL":[61.08,  4.84],\
                                 "SOR":[70.54, 22.22]}
#then event reader
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year
UT_adjustment = 1
Norway_time = time_UTC_event + UT_adjustment
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

bins_sorted,time_day_bins, time_of_event,events_collection_sorted = \
create_bins(dates_mag,dates_event, Norway_time,time_UTC_mag ,magnetic_north)
# plot_histograms(bins_sorted,time_day_bins, time_of_event)

plot_all_events(events_collection_sorted,bins_sorted)
