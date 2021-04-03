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


def plot_histograms(bins_sorted, time_day_bins, time_of_event, mag_events, latex_style = False):
    borders = [
        bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],]

    index_third, index_two_thirds = int(len(bins_sorted) / 3), int(
        len(bins_sorted) * 2 / 3)
    if latex_style:
        plt.style.use("../format_for_latex.mplstyle")

    plt.figure(0)
    plt.hist(bins_sorted, bins=30)
    plt.axvline(x=borders[0], color="r")
    plt.axvline(x=borders[1], color="r")
    plt.title(
        f"2018 {station} Max magnetometer value of a substorm event \n"+\
        f"with {mag_events} substorms collected. \n"+\
        f"borders which is {borders[0]}"+\
        f" and {borders[1]} nT")
        #f"Red lines are the lines for the borders which is {borders[0]}"+\
    plt.xlabel("minimum of the north component magnetometer [nT]")
    plt.ylabel("number of occurances")
    if latex_style:
        plt.tight_layout()
    # plt.show()
    plt.figure(1)
    plt.tight_layout()
    plt.hist(time_day_bins, bins=30)
    plt.title("Time of year when the substorm occurs")
    plt.xlabel("day of year")
    plt.ylabel("number of occurances")
    if latex_style:
        plt.tight_layout()
    # plt.show()
    plt.figure(2)
    plt.tight_layout()

    plotting_bins_array = np.concatenate(
        [time_of_event[time_of_event > 16] - 20, time_of_event[time_of_event < 16] + 4]
    )
    plt.hist(plotting_bins_array, color="b", bins=80)
    plt.title("Distrubution of what time the substorm occurs")
    plt.xlabel("time of day [UT+1]")
    plt.xticks(
        range(9),
        labels=[str(20),
                str(21),
                str(22),
                str(23),
                str(24),
                str(1),
                str(2),
                str(3),
                str(4),],
    )
    if latex_style:
        plt.tight_layout()
    # plt.show()
    plt.figure(3)
    plt.tight_layout()

    plt.hist(lat, bins=30)
    plt.title("latitude location of the substorm")
    plt.xlabel("latitude")
    plt.ylabel("Occurances")
    if latex_style:
        plt.tight_layout()
    plt.show()
    if latex_style:
        plt.style.use("default")


def plot_mag_events(events_collection_mag, bins_sorted,mag_events, latex_style = False):
    borders = [bins_sorted[int((len(bins_sorted)-1)/3)],bins_sorted[int((len(bins_sorted)-1)*2/3)]]

    index_third, index_two_thirds = int(len(events_collection_mag)/3),\
                                    int(len(events_collection_mag)*2/3)
    nr_of_xticks = hour_area*2+1
    median_event = np.nanmedian(events_collection_mag, axis = 0)
    nfive_percentile = np.nanpercentile(events_collection_mag, 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_mag, 5, axis =0)
    time = np.linspace(-(hour_area/2 -1)*60,(hour_area/2+1)*60,nr_of_xticks, dtype = int)

    if latex_style:
        plt.style.use("../format_for_latex.mplstyle")

    plt.figure(0)
    for i in range(len(events_collection_mag)):
        plt.plot(events_collection_mag[i,:], linewidth = 0.5)
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event, linewidth = 3, color = "black", label="median value")
    plt.title(f"All recorded substorms by the magnetometer in {station} in 2018 \n"+\
              f"{mag_events} substorms collected")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT]")
    plt.xticks(np.linspace(0,len(events_collection_mag)*0.915,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection_mag))
    plt.legend()
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(1)
    for i in range(index_two_thirds, len(events_collection_mag)):
        plt.plot(events_collection_mag[i,:], linewidth = 0.5)
    median_event = np.nanmedian(events_collection_mag[index_two_thirds:], axis = 0)
    nfive_percentile_third_bin = np.nanpercentile(events_collection_mag[index_two_thirds:], 95, axis =0)
    five_percentile_third_bin = np.nanpercentile(events_collection_mag[index_two_thirds:], 5, axis =0)
    plt.plot(nfive_percentile_third_bin, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile_third_bin, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event, linewidth = 3, color = "black", label="median value")
    plt.title(f"Magnetometer data of weak substorms at {station} in 2018")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT] \n (smaller than "+str(borders[1])+" nT)")
    plt.xticks(np.linspace(0,len(events_collection_mag)*0.915,nr_of_xticks),time)
    plt.legend()
    plt.ylim(-700,np.max(events_collection_mag))
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(2)
    for i in range(index_third,index_two_thirds):
        plt.plot(events_collection_mag[i,:], linewidth = 0.5)
    median_event = np.nanmedian(events_collection_mag[index_third:index_two_thirds], axis = 0)
    nfive_percentile_medium_bin = np.percentile(events_collection_mag[index_third:index_two_thirds], 95, axis =0)
    five_percentile_medium_bin = np.percentile(events_collection_mag[index_third:index_two_thirds], 5, axis =0)
    plt.plot(nfive_percentile_medium_bin, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile_medium_bin, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event, linewidth = 3, color = "black", label="median value")
    plt.title(f"Magnetometer data of medium substorms at {station} in 2018")
    plt.xlabel("minutes")
    plt.ylabel("North component B-value [nT] \n (between "+str(borders[0])+"nT and "+str(borders[1])+" nT)")
    plt.xticks(np.linspace(0,len(events_collection_mag)*0.915,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection_mag))
    plt.legend()
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(3)
    for i in range(index_third):
        plt.plot(events_collection_mag[i,:], linewidth = 0.5)
    median_event = np.nanmedian(events_collection_mag[:index_third], axis = 0)
    nfive_percentile_strong_bin = np.nanpercentile(events_collection_mag[:index_third], 95, axis =0)
    five_percentile_strong_bin = np.nanpercentile(events_collection_mag[:index_third], 5, axis =0)
    plt.plot(nfive_percentile_strong_bin, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile_strong_bin, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event, linewidth = 3, color = "black", label="median value")
    plt.title(f"Magnetometer data of strong substorms at {station} in 2018")
    plt.ylabel("North component B-value [nT] \n (bigger than "+str(borders[0])+" nT)")
    plt.xlabel("minutes")
    plt.xticks(np.linspace(0,len(events_collection_mag)*0.915,nr_of_xticks),time)
    plt.ylim(-700,np.max(events_collection_mag))
    plt.legend()
    if latex_style:
        plt.tight_layout()
    plt.show()
    if latex_style:
        plt.style.use("default")

def plot_ROTI_events(events_collection_ROTI, bins_sorted,mag_events,latex_style = False):
    borders = [bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)]]

    index_third, index_two_thirds = int(len(events_collection_ROTI) / 3), int(
        len(events_collection_ROTI) * 2 / 3)
    nr_of_xticks = hour_area*2 +1
    location = [69.66,18.94]

    time = np.linspace(-(hour_area / 2 - 1)*60, (hour_area / 2 + 1)*60, nr_of_xticks, dtype=int)
    if latex_style:
        plt.style.use("../format_for_latex.mplstyle")
    plt.figure(0)
    for i in range(len(events_collection_ROTI)):
        plt.plot(events_collection_ROTI[i,:], linewidth=0.5)

    median_event = np.nanmedian(events_collection_ROTI, axis=0)
    nfive_percentile = np.nanpercentile(events_collection_ROTI, 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_ROTI, 5, axis =0)
    plt.figure(0)
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(median_event, linewidth=3, color="black", label="median value")
    plt.title(f"All recorded substorms showed by ROTI at location {location} in 2018 \n"+\
              f"{mag_events} substorms collected")
    plt.xlabel("minutes")
    plt.ylabel("ROTI values [TEC/min]")

    plt.xticks(np.linspace(0, 0.19*len(events_collection_ROTI), nr_of_xticks), time)
    plt.legend()
    plt.ylim(0,10)
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(1)
    for i in range(index_two_thirds, len(events_collection_ROTI)):
        plt.plot(events_collection_ROTI[i, :], linewidth=0.5)
    median_event = np.nanmedian(events_collection_ROTI[index_two_thirds:], axis = 0)
    nfive_percentile = np.nanpercentile(events_collection_ROTI[index_two_thirds:], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_ROTI[index_two_thirds:], 5, axis =0)
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(median_event, linewidth=3, color="black", label="median value")
    plt.title(f"ROTI of weak substorms at {station} in 2018")
    plt.xlabel("minutes")
    plt.ylabel("ROTI values [TEC/min]")
    plt.xticks(np.linspace(0, 0.19*len(events_collection_ROTI), nr_of_xticks), time)
    plt.legend()
    plt.ylim(0,10)
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(2)
    for i in range(index_third, index_two_thirds):
        plt.plot(events_collection_ROTI[i,:], linewidth=0.5)
    median_event = np.nanmedian(events_collection_ROTI[index_third:index_two_thirds], axis = 0)
    nfive_percentile = np.nanpercentile(events_collection_ROTI[index_third:index_two_thirds], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_ROTI[index_third:index_two_thirds], 5, axis =0)
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5th percentile")
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(median_event, linewidth=3, color="black", label="median value" )
    plt.title(f"ROTI of medium substorms at {station} in 2018")
    plt.xlabel("minutes")
    plt.ylabel("ROTI values [TEC/min]")
    plt.xticks(np.linspace(0, 0.19*len(events_collection_ROTI), nr_of_xticks), time)
    plt.ylim(0,10)
    plt.legend()
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(3)
    for i in range(index_third):
        plt.plot(events_collection_ROTI[i,:], linewidth=0.5)
    median_event = np.nanmedian(events_collection_ROTI[:index_third], axis = 0)
    nfive_percentile = np.nanpercentile(events_collection_ROTI[:index_third], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_ROTI[:index_third], 5, axis =0)
    plt.plot(median_event, linewidth = 3, color = "black", label="median value")
    plt.plot(nfive_percentile, linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile, linewidth = 3, color = "red", label="5th percentile")
    plt.title(f"ROTI of strong substorms at {station} in 2018")
    plt.xlabel("minutes")
    plt.ylabel("ROTI values [TEC/min]")
    plt.xticks(np.linspace(0, 0.19*len(events_collection_ROTI), nr_of_xticks), time)
    plt.legend()
    plt.ylim(0,10)
    if latex_style:
        plt.tight_layout()
    plt.show()
    if latex_style:
        plt.style.use("default")

def plot_gps_events(events_collection_gps, bins_sorted,GPS_events, latex_style = False):
    borders = [bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],]

    index_third, index_two_thirds = int(len(events_collection_gps) / 3), int(
        len(events_collection_gps) * 2 / 3)
    nr_of_xticks = hour_area*2 + 1
    station = "TRM"
    time = np.linspace(-(hour_area / 2 - 1)*60, (hour_area / 2 + 1)*60, nr_of_xticks,dtype=int)

    if latex_style:
        plt.style.use("../format_for_latex.mplstyle")

    plt.figure(0)

    steps_gps = 60
    for i in range(len(events_collection_gps)):
        plt.plot(events_collection_gps[i, ::steps_gps], linewidth=0.5)
    median_event = np.nanmedian(events_collection_gps, axis=0)
    nfive_percentile = np.nanpercentile(events_collection_gps, 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_gps, 5, axis =0)
    plt.plot(nfive_percentile[::steps_gps], linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile[::steps_gps], linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event[::steps_gps], linewidth = 3, color="black", label="median value")
    plt.title(f"All recorded substorms by the gps receivers in {station} in 2018\n"+\
              f"{GPS_events} substorms collected")
    plt.xlabel("minutes")
    plt.ylabel("noise values from the NMEA")
    plt.ylim(5e-5,1)
    plt.xticks(np.linspace(0, len(events_collection_gps)*60/steps_gps, nr_of_xticks), time)
    plt.legend()
    plt.yscale("log")
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(1)
    for i in range(index_two_thirds, len(events_collection_gps)):
        plt.plot(events_collection_gps[i, ::steps_gps], linewidth=0.5)
    nfive_percentile = np.nanpercentile(events_collection_gps[index_two_thirds:], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_gps[index_two_thirds:], 5, axis =0)
    median_event = np.nanmedian(events_collection_gps[index_two_thirds:], axis=0)
    plt.plot(nfive_percentile[::steps_gps], linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile[::steps_gps], linewidth = 3, color = "red", label="5th percentile")
    plt.plot(median_event[::steps_gps], linewidth = 3, color = "black", label="median value")
    plt.title("Weak substorms by the gps receiver in " + station + " in 2018")
    plt.xlabel("minutes")
    plt.ylabel("noise values from the NMEA ")
    plt.xticks(np.linspace(0, len(events_collection_gps), nr_of_xticks), time)
    plt.legend()
    plt.ylim(5e-5,1)
    plt.yscale("log")
    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(2)
    for i in range(index_third, index_two_thirds):
        plt.plot(events_collection_gps[i, ::steps_gps], linewidth=0.5)
    nfive_percentile = np.nanpercentile(events_collection_gps[index_third:index_two_thirds], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_gps[index_third:index_two_thirds], 5, axis =0)
    median_event = np.nanmedian(events_collection_gps[index_third:index_two_thirds], axis=0)
    plt.plot(median_event[::steps_gps], linewidth = 3, color = "black", label="median value")
    plt.plot(nfive_percentile[::steps_gps], linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile[::steps_gps], linewidth = 3, color = "red", label="5th percentile")
    plt.title("Medium substorms by the gps receiver in " + station + " in 2018")
    plt.xlabel("minutes")
    plt.ylabel("noise values from the NMEA")
    plt.legend()
    plt.xticks(np.linspace(0, len(events_collection_gps), nr_of_xticks), time)
    plt.ylim(5e-5,1)

    plt.yscale("log")

    if latex_style:
        plt.tight_layout()
    # plt.show()

    plt.figure(3)
    for i in range(index_third):
        plt.plot(events_collection_gps[i, ::steps_gps], linewidth=0.5)

    median_event = np.nanmedian(events_collection_gps[:index_third], axis = 0)
    nfive_percentile = np.nanpercentile(events_collection_gps[:index_third], 95, axis =0)
    five_percentile = np.nanpercentile(events_collection_gps[:index_third], 5, axis =0)
    plt.plot(median_event[::steps_gps], linewidth = 3, color = "black", label="median value")
    plt.plot(nfive_percentile[::steps_gps], linewidth = 3, color = "green", label="95th percentile")
    plt.plot(five_percentile[::steps_gps], linewidth = 3, color = "red", label="5th percentile")
    plt.title("strong substorms by the gps receiver in " + station + " in 2018")
    plt.ylabel("noise values from the NMEA")
    plt.xlabel("minutes")
    plt.xticks(np.linspace(0, len(events_collection_gps), nr_of_xticks), time)
    plt.legend()
    plt.yscale("log")
    plt.ylim(5e-5,1)
    if latex_style:
        plt.tight_layout()
    plt.show()
    if latex_style:
        plt.style.use("default")

def plot_all_data_events(mag,ROTI,gps,latex_style=False):

    start_x, end_x = -(hour_area / 2 - 1)*60, (hour_area / 2 + 1)*60
    nr_of_xticks = hour_area*2+1
    time = np.linspace(start_x, end_x, nr_of_xticks,dtype=int)
    location = [69.66,18.94]

    fig1,ax1 = plt.subplots(3,1, sharex = True)
    fig1.suptitle(f"All data comparison")
    if latex_style:
        plt.style.use("../format_for_latex.mplstyle")

    """
    all bins
    """
    median_event = np.nanmedian(mag, axis = 0)
    nfive_percentile = np.nanpercentile(mag, 95, axis =0)
    five_percentile = np.nanpercentile(mag, 5, axis =0)
    for i in range(len(mag)):
        ax1[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),mag[i,:], linewidth = 0.5 )
    ax1[0].plot(np.zeros(2000),np.linspace(-1000,np.max(mag),2000),"b", linewidth = 1.5 )
    ax1[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax1[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),five_percentile, linewidth = 3, color = "red")
    ax1[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),median_event, linewidth = 3, color = "black")
    ax1[0].set_ylabel("North B-value [nT]")
    ax1[0].set_xticks([])
    ax1[0].set_ylim(-600,np.max(mag))
    ax1[0].legend()

    for i in range(len(ROTI)):
        ax1[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),ROTI[i,:], linewidth=0.5)

    median_event = np.nanmedian(ROTI, axis=0)
    nfive_percentile = np.nanpercentile(ROTI, 95, axis =0)
    five_percentile = np.nanpercentile(ROTI, 5, axis =0)
    ax1[1].plot(np.zeros(2000),np.linspace(0,10,2000),"b", linewidth =1.5)
    ax1[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),five_percentile, linewidth = 3, color = "red")
    ax1[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax1[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),median_event, linewidth=3, color="black")
    ax1[1].set_ylabel("ROTI values [TEC/min]")
    ax1[1].set_xticks([])
    ax1[1].set_ylim(0,10)

    for i in range(len(gps)):
        ax1[2].plot(np.linspace(start_x, end_x,len(gps[0,:]))[::60],gps[i, ::60], linewidth=0.5)
    median_event = np.nanmedian(gps, axis=0)
    nfive_percentile = np.nanpercentile(gps, 95, axis =0)
    five_percentile = np.nanpercentile(gps, 5, axis =0)
    ax1[2].plot(np.zeros(2000),np.linspace(5e-5,1,2000),"b", linewidth =1.5)
    ax1[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],nfive_percentile[::60], linewidth = 3, color = "green", label="95th percentile")
    ax1[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],five_percentile[::60], linewidth = 3, color = "red", label="5th percentile")
    ax1[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],median_event[::60], linewidth = 3, color="black", label="median value")
    ax1[2].set_xlabel("minutes")
    ax1[2].set_ylabel("noise from NMEA")
    ax1[2].set_ylim(5e-5,1)
    ax1[2].set_xticks(time)
    ax1[2].legend()
    ax1[2].set_yscale("log")
    if latex_style:
        plt.tight_layout()

    """
    Weak bin
    """
    borders = [bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],]

    index_third, index_two_thirds = int(len(gps) / 3), int(
        len(gps) * 2 / 3)

    fig2,ax2 = plt.subplots(3,1, sharex = True)
    fig2.suptitle(f"Weak bin comparison of data")
    median_event = np.nanmedian(mag[index_two_thirds:], axis = 0)
    nfive_percentile = np.nanpercentile(mag[index_two_thirds:], 95, axis =0)
    five_percentile = np.nanpercentile(mag[index_two_thirds:], 5, axis =0)

    for i in range(index_two_thirds,len(mag)):
        ax2[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),mag[i,:], linewidth = 0.5)

    ax2[0].plot(np.zeros(2000),np.linspace(-300,np.max(mag),2000),"b", linewidth =2)
    ax2[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax2[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),five_percentile, linewidth = 3, color = "red")
    ax2[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),median_event, linewidth = 3, color = "black")
    ax2[0].set_ylabel("North B-value [nT]")
    ax2[0].set_xticks([])
    ax2[0].set_ylim(-600,np.max(mag))
    ax2[0].legend()

    for i in range(index_two_thirds,len(ROTI)):
        ax2[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),ROTI[i,:], linewidth=0.5)

    median_event = np.nanmedian(ROTI[index_two_thirds:], axis=0)
    nfive_percentile = np.nanpercentile(ROTI[index_two_thirds:], 95, axis =0)
    five_percentile = np.nanpercentile(ROTI[index_two_thirds:], 5, axis =0)
    ax2[1].plot(np.zeros(2000),np.linspace(0,10,2000),"b", linewidth =2)
    ax2[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),five_percentile, linewidth = 3, color = "red")
    ax2[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax2[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),median_event, linewidth=3, color="black")
    ax2[1].set_ylabel("ROTI values [TEC/min]")
    ax2[1].set_xticks([])
    ax2[1].set_ylim(0,10)

    for i in range(index_two_thirds,len(gps)):
        ax2[2].plot(np.linspace(start_x, end_x,len(gps[0,:]))[::60],gps[i, ::60], linewidth=0.5)
    median_event = np.nanmedian(gps[index_two_thirds:], axis=0)
    nfive_percentile = np.nanpercentile(gps[index_two_thirds:], 95, axis =0)
    five_percentile = np.nanpercentile(gps[index_two_thirds:], 5, axis =0)
    ax2[2].plot(np.zeros(2000),np.linspace(5e-5,1,2000),"b", linewidth =2)
    ax2[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],nfive_percentile[::60], linewidth = 3, color = "green", label="95th percentile")
    ax2[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],five_percentile[::60], linewidth = 3, color = "red", label="5th percentile")
    ax2[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],median_event[::60], linewidth = 3, color="black", label="median value")
    ax2[2].set_xlabel("minutes")
    ax2[2].set_ylabel("noise from NMEA")
    ax2[2].set_ylim(5e-5,1)
    ax2[2].set_xticks(time)
    ax2[2].legend()
    ax2[2].set_yscale("log")
    if latex_style:
        plt.tight_layout()

    """
    Medium bin
    """
    fig3,ax3 = plt.subplots(3,1, sharex = True)
    fig3.suptitle(f"Medium bin comparison of data")
    median_event = np.nanmedian(mag[index_third:index_two_thirds], axis = 0)
    nfive_percentile = np.nanpercentile(mag[index_third:index_two_thirds], 95, axis =0)
    five_percentile = np.nanpercentile(mag[index_third:index_two_thirds], 5, axis =0)

    for i in range(index_third,index_two_thirds):
        ax3[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),mag[i,:], linewidth = 0.5)

    ax3[0].plot(np.zeros(2000),np.linspace(-300,np.max(mag),2000),"b", linewidth =2)
    ax3[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax3[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),five_percentile, linewidth = 3, color = "red")
    ax3[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),median_event, linewidth = 3, color = "black")
    ax3[0].set_ylabel("North B-value [nT]")
    ax3[0].set_xticks([])
    ax3[0].set_ylim(-600,np.max(mag))
    ax3[0].legend()

    for i in range(index_third,index_two_thirds):
        ax3[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),ROTI[i,:], linewidth=0.5)

    median_event = np.nanmedian(ROTI[index_third:index_two_thirds], axis=0)
    nfive_percentile = np.nanpercentile(ROTI[index_third:index_two_thirds], 95, axis =0)
    five_percentile = np.nanpercentile(ROTI[index_third:index_two_thirds], 5, axis =0)
    ax3[1].plot(np.zeros(2000),np.linspace(0,10,2000),"b", linewidth =2)
    ax3[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),five_percentile, linewidth = 3, color = "red")
    ax3[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax3[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),median_event, linewidth=3, color="black")
    ax3[1].set_ylabel("ROTI values [TEC/min]")
    ax3[1].set_xticks([])
    ax3[1].set_ylim(0,10)

    for i in range(index_third,index_two_thirds):
        ax3[2].plot(np.linspace(start_x, end_x,len(gps[0,:]))[::60],gps[i, ::60], linewidth=0.5)
    median_event = np.nanmedian(gps[index_third:index_two_thirds], axis=0)
    nfive_percentile = np.nanpercentile(gps[index_third:index_two_thirds], 95, axis =0)
    five_percentile = np.nanpercentile(gps[index_third:index_two_thirds], 5, axis =0)
    ax3[2].plot(np.zeros(2000),np.linspace(5e-5,1,2000),"b", linewidth =2)
    ax3[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],nfive_percentile[::60], linewidth = 3, color = "green", label="95th percentile")
    ax3[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],five_percentile[::60], linewidth = 3, color = "red", label="5th percentile")
    ax3[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],median_event[::60], linewidth = 3, color="black", label="median value")
    ax3[2].set_xlabel("minutes")
    ax3[2].set_ylabel("noise from NMEA")
    ax3[2].set_ylim(5e-5,1)
    ax3[2].set_xticks(time)
    ax3[2].legend()
    ax3[2].set_yscale("log")
    if latex_style:
        plt.tight_layout()

    """
    Strong bin
    """
    fig4,ax4 = plt.subplots(3,1, sharex = True)
    fig4.suptitle(f"Strong bin comparison of data")
    median_event = np.nanmedian(mag[:index_third], axis = 0)
    nfive_percentile = np.nanpercentile(mag[:index_third], 95, axis =0)
    five_percentile = np.nanpercentile(mag[:index_third], 5, axis =0)

    for i in range(index_third):
        ax4[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),mag[i,:], linewidth = 0.5)

    ax4[0].plot(np.zeros(2000),np.linspace(-700,np.max(mag),2000),"b", linewidth =2)
    ax4[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax4[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),five_percentile, linewidth = 3, color = "red")
    ax4[0].plot(np.linspace(start_x,end_x, len(mag[0,:])),median_event, linewidth = 3, color = "black")
    ax4[0].set_ylabel("North B-value [nT]")
    ax4[0].set_xticks([])
    ax4[0].set_ylim(-600,np.max(mag))
    ax4[0].legend()

    for i in range(index_third):
        ax4[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),ROTI[i,:], linewidth=0.5)

    median_event = np.nanmedian(ROTI[:index_third], axis=0)
    nfive_percentile = np.nanpercentile(ROTI[:index_third], 95, axis =0)
    five_percentile = np.nanpercentile(ROTI[:index_third], 5, axis =0)
    ax4[1].plot(np.zeros(2000),np.linspace(0,10,2000),"b", linewidth =2)
    ax4[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),five_percentile, linewidth = 3, color = "red")
    ax4[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),nfive_percentile, linewidth = 3, color = "green")
    ax4[1].plot(np.linspace(start_x,end_x, len(ROTI[0,:])),median_event, linewidth=3, color="black")
    ax4[1].set_ylabel("ROTI values [TEC/min]")
    ax4[1].set_xticks([])
    ax4[1].set_ylim(0,10)

    for i in range(index_third):
        ax4[2].plot(np.linspace(start_x, end_x,len(gps[0,:]))[::60],gps[i, ::60], linewidth=0.5)
    median_event = np.nanmedian(gps[:index_third], axis=0)
    nfive_percentile = np.nanpercentile(gps[:index_third], 95, axis =0)
    five_percentile = np.nanpercentile(gps[:index_third], 5, axis =0)
    ax4[2].plot(np.zeros(2000),np.linspace(5e-5,1,2000),"b", linewidth =2)
    ax4[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],nfive_percentile[::60], linewidth = 3, color = "green", label="95th percentile")
    ax4[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],five_percentile[::60], linewidth = 3, color = "red", label="5th percentile")
    ax4[2].plot(np.linspace(start_x,end_x, len(gps[0,:]))[::60],median_event[::60], linewidth = 3, color="black", label="median value")
    ax4[2].set_xlabel("minutes")
    ax4[2].set_ylabel("noise from NMEA")
    ax4[2].set_ylim(5e-5,1)
    ax4[2].set_xticks(time)
    ax4[2].legend()
    ax4[2].set_yscale("log")
    if latex_style:
        plt.tight_layout()


    plt.show()


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

def statistical_reduction_of_data(gps_data,start_index,end_index):
    originial_shape = gps_data.shape
    gps_data = gps_data.flatten()
    print(gps_data[start_index:end_index])
    median1 = np.nanmedian(gps_data[start_index:end_index])
    median2 = np.nanmedian(gps_data[:start_index])
    ratio = median1/median2
    print("ratio",ratio)
    gps_data[start_index:end_index] = gps_data[start_index:end_index]/ratio
    gps_data = gps_data.reshape(365,50500)
    return gps_data




def load_gps_noise():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        time = np.load(file)
        noise = np.load(file)
    start_index_weird_time = 7649115 -50500
    end_index_weird_time = 7858915 -50500
    noise = statistical_reduction_of_data(noise,start_index_weird_time,end_index_weird_time)
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
mag_collection_sorted,ROTI_event_sorted,noise_gps_sorted,time_gps_sorted, \
mag_events, GPS_events \
= create_bins_gps_ROTI_mag(hour_area,dates_mag,dates_event,Norway_time
                              ,magnetic_north,
                              gps_noise,time_axis_gps,
                              time_ROTI_TRO, ROTI_biint_TRO)
print(noise_gps_sorted.shape, "shape noise_gps_sorted")
print(time_gps_sorted.shape, "shape time_gps_sorted")


def clean_nans_gps_noise(time_gps_sorted,noise_gps_sorted):
    r = pd.date_range(start="2018-01-01T00:00:00", end="2018-01-01T04:00:00", freq="S")
    new_time = np.zeros((257,4*60*60+1))*np.nan
    new_gps_noise = np.zeros((257,4*60*60+1))*np.nan
    for i in range(257):
        df = pd.DataFrame(r, columns = ["time"])
        df["gps_noise"] = np.nan
        print(i/257*100)
        for ii in range(36000):
            if not np.isnan(time_gps_sorted[i,ii]):
                index = round(time_gps_sorted[i,ii]*3600)
                # print(index)
                # print(noise_gps_sorted[i,ii])
                # print("df before", df)
                df.gps_noise[index] = noise_gps_sorted[i,ii]
                # print("df after", df)

        # print(df["gps_noise"])
        new_time[i,:] = date_to_days(df["time"])
        new_gps_noise[i,:] = df["gps_noise"]
    file_path = "../../data_storage_arrays/filtered_NMEA_data_TRM.txt"
    with open(file_path,"wb") as file:
        np.save(file,new_time)
        np.save(file,new_gps_noise)

def load_cleaned_gps_noise():
    file_path = "../../data_storage_arrays/filtered_NMEA_data_TRM.txt"
    with open(file_path,"rb") as file:
        a = np.load(file)
        b = np.load(file)

    return a, b

# clean_nans_gps_noise(time_gps_sorted,noise_gps_sorted)
new_time, new_gps_noise = load_cleaned_gps_noise()

#########################plotting data#########################
# plot_histograms(bins_sorted,time_day_bins, time_of_event, mag_events, latex_style =True)
plot_mag_events(mag_collection_sorted,bins_sorted,mag_events ,latex_style = False)
plot_ROTI_events(ROTI_event_sorted,bins_sorted, mag_events ,latex_style = False)
plot_gps_events(new_gps_noise,bins_sorted, GPS_events, latex_style = False)
plot_all_data_events(mag_collection_sorted,ROTI_event_sorted,new_gps_noise,latex_style= False)
