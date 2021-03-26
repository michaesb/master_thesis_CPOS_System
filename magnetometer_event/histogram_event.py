import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys, time
import pandas as pd
from numba import njit, prange
from collections import Counter

sys.path.insert(0, "../")  # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData
from magnetometer_event.creating_bins import create_bins_gps_ROTI_mag
from noise_gps_function import run_NMEA_data


def style_chooser(style,i):
    if style == "downwards":
        if 4>i:
            plt.subplot(4,2,1+i*2,)
        else:
            plt.subplot(4,2,2*i-6)
        if i==3 or i==7:
            pass
        else:
            plt.xticks([])
    elif style == "right":
        plt.subplot(4,2,i+1)
        if i>5:
            pass
        else:
            plt.xticks([])
    else:
        raise TypeError("need to select a correct way to plot the histogram"+\
                        f", not {style}")


def plot_histogram_event_mag(events_collection, bins_sorted, mag_events,fancy_latex = False):

        borders = [bins_sorted[int((len(bins_sorted)-1)/3)],bins_sorted[int((len(bins_sorted)-1)*2/3)]]

        index_third, index_two_thirds = int(len(events_collection)/3),\
                                        int(len(events_collection)*2/3)

        if fancy_latex:
            plt.style.use("../format_for_latex.mplstyle")

        style = "downwards"
        nr_plots= 8
        plt.figure(0)
        plt.suptitle(f"All recorded substorms by the magnetometer at {station} in 2018."+\
                            f"\n {mag_events} substorms collected ")
        for i in range(0,nr_plots):
            style_chooser(style,i)
            plt.hist(events_collection[:,i*30], bins = 40, range=(-800,100))
            plt.title(f"{(i-2)*30} min")
            plt.ylim(0,70)

            plt.tight_layout()

        plt.figure(1)
        plt.suptitle(f"Magnetometer data of weak substorms at {station} in 2018")
        for i in range(0,nr_plots):
            style_chooser(style,i)
            plt.hist(events_collection[index_two_thirds:,i*30], bins = 40, range=(-800,100) )
            plt.title(f"{(i-2)*30} min")
            plt.ylim(0,30)
            plt.tight_layout()

        plt.figure(2)
        plt.suptitle(f"Magnetometer data of medium substorms at {station} in 2018")
        for i in range(0,nr_plots):
            style_chooser(style,i)
            plt.hist(events_collection[index_third:index_two_thirds,i*30], bins = 40, range=(-800,100))
            plt.title(f"{(i-2)*30} min")
            plt.ylim(0,30)
            plt.tight_layout()

        # plt.show()
        plt.figure(3)
        plt.suptitle(f"Magnetometer data of strong substorms at at {station} in 2018")
        for i in range(0,nr_plots):
            style_chooser(style,i)
            plt.hist(events_collection[:index_third,i*30], bins = 40, range=(-800,100))
            plt.title(f"{(i-2)*30} min")
            plt.xlim(-800,50)
            plt.ylim(0,30)
            plt.tight_layout()
        plt.show()

        if fancy_latex:
            plt.style.use("default")


def plot_histogram_event_ROTI(events_collection_ROTI, bins_sorted,mag_events,fancy_latex = False):
    borders = [bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)]]

    index_third, index_two_thirds = int(len(events_collection_ROTI) / 3), int(
        len(events_collection_ROTI) * 2 / 3)
    location = [69.66,18.94]

    if fancy_latex:
        plt.style.use("../format_for_latex.mplstyle")
    nr_plots= 8
    times_of_interest = [-60,0,5,10,15,30,60,120]
    style ="downwards"
    nr_bins= 30
    plt.figure(0)
    plt.suptitle(f"All recorded substorms by the ROTI at {station} in 2018." +\
                    f"\n {mag_events} substorms collected ")
    for i in range(nr_plots):
        style_chooser(style,i)
        plt.hist(events_collection_ROTI[:,int((60+times_of_interest[i])/5)], bins = nr_bins,range=(0,5))
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0,80)
        plt.tight_layout()

    plt.figure(1)
    plt.suptitle(f"ROTI of weak substorms at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style,i)
        plt.hist(events_collection_ROTI[index_two_thirds:,int((60+times_of_interest[i])/5)], bins = nr_bins,range=(0,5))
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0,25)
        plt.tight_layout()


    # plt.show()
    plt.figure(2)
    plt.suptitle(f"ROTI of medium substorms at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style,i)
        plt.hist(events_collection_ROTI[index_third:index_two_thirds,int((60+times_of_interest[i])/5)], bins = nr_bins,range=(0,5))
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0,25)
        plt.tight_layout()

    # plt.show()
    plt.figure(3)
    plt.suptitle(f"ROTI of strong substorms at at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style,i)
        plt.hist(events_collection_ROTI[:index_third,int((60+times_of_interest[i])/5)], bins = nr_bins,range=(0,5))
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0,25)
        plt.tight_layout()
    plt.show()

    if fancy_latex:
        plt.style.use("default")


def plot_histogram_event_GPS(events_collection_gps,time_gps_sorted, bins_sorted,GPS_events ,fancy_latex = False):

    borders = [bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],]

    index_third, index_two_thirds = int(len(events_collection_gps) / 3), int(
        len(events_collection_gps) * 2 / 3)
    station = "TRM"
    style ="downwards"
    times_of_interest = [-60,0,5,10,15,30,60,120]
    xmax,xmin = 0,0.05
    nr_bins=30
    if fancy_latex:
        plt.style.use("../format_for_latex.mplstyle")

    for i in range(0,8):
        style_chooser(style,i)
        plt.hist(events_collection_gps[:,int((times_of_interest[i]+60)/60*1800)],bins=nr_bins,range=(0,0.1))
        plt.title(f"{times_of_interest[i]} min ")
        plt.yscale("log")
        plt.tight_layout()
    plt.show()
    if fancy_latex:
        plt.style.use("default")


obj_event = ReadSubstormEvent()
obj_mag = ReadMagnetomerData()

save_ram_memory = True

try:
    laptop_path = "/scratch/michaesb/"
    path_event = laptop_path + "substorm_event_list_2018.csv"
    path_mag = laptop_path + "20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)

    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path,"rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        dates_mag,location_long,location_lat,geographic_north,\
        geographic_east,geographic_z,magnetic_north,magnetic_east,magnetic_z\
        = obj_mag.receiver_specific_data(station)

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/data_ssd/data"
    path_event = desktop_path + "/substorm_event_list_2018.csv"
    path_mag = desktop_path + "/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)
    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path,"rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        dates_mag,location_long,location_lat,geographic_north,\
        geographic_east,geographic_z,magnetic_north,magnetic_east,magnetic_z\
        = obj_mag.receiver_specific_data(station)


########################### magnetometer reader  ##########################
station = "TRM"
stations_dictionary_GEO_coord = {
    "KIL": [69.02, 20.79],
    "TRM": [69.66, 18.94],
    "ABK": [68.35, 18.82],
    "AND": [69.30, 16.03],
    "DOB": [62.07, 9.11],
    "DON": [66.11, 12.50],
    "JCK": [66.40, 16.98],
    "KAR": [59.21, 5.24],
    "MAS": [69.46, 23.70],
    "NOR": [71.09, 25.79],
    "RVK": [64.94, 10.99],
    "SOL": [61.08, 4.84],
    "SOR": [70.54, 22.22],
}

########################## event reader  #############################
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year
dates_event = pd.to_datetime(dates_event,format="%Y-%m-%d %H:%M:%S")


Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(
lat, mag_time, Norway_time, dates_event, verbose = False)
# raise Exception("hello there")

########################## gps noise  ##################################


def create_fake_noise():
    n = 50200
    time_axis_gps = np.zeros((365, n + 365)) * np.nan
    gps_noise = np.zeros((365, n + 365)) * np.nan
    for i in range(365):
        time_axis_gps[i, : n + i] = np.linspace(0, 24, n + i)
        gps_noise[i, : n + i] = np.ones(n+i)*(i+1)
        print(gps_noise[i,:])
    return time_axis_gps, gps_noise

def load_gps_noise():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        time = np.load(file)
        noise = np.load(file)
    return time, noise

# time_axis_gps,gps_noise = run_NMEA_data(365,"TRM")
# time_axis_gps, gps_noise = create_fake_noise()
time_axis_gps,gps_noise = load_gps_noise()

########################## ROTI  ##################################

def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path,"rb") as file:
        time = np.load(file)
        ROTI_biint = np.load(file)
    return time, ROTI_biint

time_ROTI_TRO, ROTI_biint_TRO = load_ROTI_data()


########################## creating bins ###################################
hour_area = 4
bins_sorted,time_day_bins,time_of_event,\
events_collection_sorted,ROTI_event_sorted,noise_gps_sorted,time_gps_sorted, \
mag_events, GPS_events \
= create_bins_gps_ROTI_mag(hour_area,dates_mag,dates_event,Norway_time
                              ,magnetic_north,
                              gps_noise,time_axis_gps,
                              time_ROTI_TRO, ROTI_biint_TRO)

def load_cleaned_gps_noise():
    file_path = "../../data_storage_arrays/filtered_NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        a = np.load(file)
        b = np.load(file)

    return a, b
# clean_nans_gps_noise(time_gps_sorted,noise_gps_sorted)
new_time, new_gps_noise = load_cleaned_gps_noise()

# noise_gps_sorted =noise_gps_sorted[abs(np.isnan(noise_gps_sorted))-1]
# time_gps_sorted =time_gps_sorted[abs(np.isnan(time_gps_sorted))-1]
#########################plotting data#########################

plot_histogram_event_mag(events_collection_sorted,bins_sorted, mag_events, fancy_latex = False)
plot_histogram_event_ROTI(ROTI_event_sorted,bins_sorted, mag_events, fancy_latex = False)
plot_histogram_event_GPS(new_gps_noise,new_time, bins_sorted,GPS_events,fancy_latex = False)
