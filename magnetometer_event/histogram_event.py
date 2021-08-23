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


def style_chooser(style, i):
    if style == "downwards":
        if 4 > i:
            plt.subplot(
                4,
                2,
                1 + i * 2,
            )
        else:
            plt.subplot(4, 2, 2 * i - 6)
        if i == 3 or i == 7:
            pass
        else:
            plt.xticks([])
    elif style == "right":
        plt.subplot(4, 2, i + 1)
        if i > 5:
            pass
        else:
            plt.xticks([])
    else:
        raise TypeError(
            "need to select a correct way to plot the histogram" + f", not {style}"
        )


def plot_histogram_event_mag(mag, bins_sorted, mag_events, fancy_latex=False):

    borders = [
        bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],
    ]

    index_third, index_two_thirds = int(len(mag) / 3), int(len(mag) * 2 / 3)

    if fancy_latex:
        plt.style.use("../format_for_latex_standard.mplstyle")

    style = "downwards"
    nr_plots = 8
    plt.figure(0)
    plt.suptitle(
        f"All recorded substorms by the magnetometer at {station} in 2018."
        + f"\n {mag_events} substorms collected "
    )
    for i in range(0, nr_plots):
        style_chooser(style, i)
        plt.hist(mag[:, i * 30], bins=40, range=(-800, 100))
        plt.title(f"{(i-2)*30} min")
        plt.ylim(0, 70)
        five_percentile = np.nanpercentile(mag, 5, axis=0)
        nfive_percentile = np.nanpercentile(mag, 95, axis=0)
        plt.axvline(
            five_percentile[i * 30], color="red", linestyle="dashed", linewidth=1
        )
        plt.axvline(
            nfive_percentile[i * 30], color="green", linestyle="dashed", linewidth=1
        )
        plt.tight_layout()

    plt.figure(1)
    plt.suptitle(f"Magnetometer data of weak substorms at {station} in 2018")
    for i in range(0, nr_plots):
        style_chooser(style, i)
        plt.hist(mag[index_two_thirds:, i * 30], bins=40, range=(-800, 100))
        plt.title(f"{(i-2)*30} min")
        plt.ylim(0, 30)
        five_percentile = np.nanpercentile(mag[index_two_thirds:], 5, axis=0)
        nfive_percentile = np.nanpercentile(mag[index_two_thirds:], 95, axis=0)
        plt.axvline(
            five_percentile[i * 30], color="red", linestyle="dashed", linewidth=1
        )
        plt.axvline(
            nfive_percentile[i * 30], color="green", linestyle="dashed", linewidth=1
        )
        plt.tight_layout()

    plt.figure(2)
    plt.suptitle(f"Magnetometer data of medium substorms at {station} in 2018")
    for i in range(0, nr_plots):
        style_chooser(style, i)
        plt.hist(mag[index_third:index_two_thirds, i * 30], bins=40, range=(-800, 100))
        plt.title(f"{(i-2)*30} min")
        plt.ylim(0, 30)
        five_percentile = np.nanpercentile(mag[index_third:index_two_thirds], 5, axis=0)
        nfive_percentile = np.nanpercentile(
            mag[index_third:index_two_thirds], 95, axis=0
        )
        plt.axvline(
            five_percentile[i * 30], color="red", linestyle="dashed", linewidth=1
        )
        plt.axvline(
            nfive_percentile[i * 30], color="green", linestyle="dashed", linewidth=1
        )
        plt.tight_layout()

    # plt.show()
    plt.figure(3)
    plt.suptitle(f"Magnetometer data of strong substorms at at {station} in 2018")
    for i in range(0, nr_plots):
        style_chooser(style, i)
        plt.hist(mag[:index_third, i * 30], bins=40, range=(-800, 100))
        plt.title(f"{(i-2)*30} min")
        plt.xlim(-800, 50)
        plt.ylim(0, 30)
        five_percentile = np.nanpercentile(mag[:index_third], 5, axis=0)
        nfive_percentile = np.nanpercentile(mag[:index_third], 95, axis=0)
        plt.axvline(
            five_percentile[i * 30], color="red", linestyle="dashed", linewidth=1
        )
        plt.axvline(
            nfive_percentile[i * 30], color="green", linestyle="dashed", linewidth=1
        )
        plt.tight_layout()
    plt.show()

    if fancy_latex:
        plt.style.use("default")


def plot_histogram_event_ROTI(
    events_collection_ROTI, bins_sorted, mag_events, fancy_latex=False
):
    borders = [
        bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],
    ]

    index_third, index_two_thirds = int(len(events_collection_ROTI) / 3), int(
        len(events_collection_ROTI) * 2 / 3
    )
    location = [69.66, 18.94]

    if fancy_latex:
        plt.style.use("../format_for_latex_standard.mplstyle")
    nr_plots = 8
    times_of_interest = [-60, 0, 5, 10, 15, 30, 60, 120]
    style = "downwards"
    nr_bins = 80
    plt.figure(0)
    plt.suptitle(
        f"All recorded substorms by the ROTI at {station} in 2018."
        + f"\n {mag_events} substorms collected "
    )
    for i in range(nr_plots):
        style_chooser(style, i)
        plt.hist(
            events_collection_ROTI[:, int((60 + times_of_interest[i]) / 5)],
            bins=nr_bins,
            range=(0, 7),
        )
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0, 50)
        five_percentile = np.nanpercentile(events_collection_ROTI, 5, axis=0)
        nfive_percentile = np.nanpercentile(events_collection_ROTI, 95, axis=0)
        plt.axvline(
            five_percentile[int((60 + times_of_interest[i]) / 5)],
            color="red",
            linestyle="dashed",
            linewidth=1,
        )
        plt.axvline(
            nfive_percentile[int((60 + times_of_interest[i]) / 5)],
            color="green",
            linestyle="dashed",
            linewidth=1,
        )
        plt.tight_layout()

    plt.figure(1)
    plt.suptitle(f"ROTI of weak substorms at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style, i)
        plt.hist(
            events_collection_ROTI[
                index_two_thirds:, int((60 + times_of_interest[i]) / 5)
            ],
            bins=nr_bins,
            range=(0, 7),
        )
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0, 20)
        five_percentile = np.nanpercentile(
            events_collection_ROTI[index_two_thirds:], 5, axis=0
        )
        nfive_percentile = np.nanpercentile(
            events_collection_ROTI[index_two_thirds:], 95, axis=0
        )
        plt.axvline(
            five_percentile[int((60 + times_of_interest[i]) / 5)],
            color="red",
            linestyle="dashed",
            linewidth=1,
        )
        plt.axvline(
            nfive_percentile[int((60 + times_of_interest[i]) / 5)],
            color="green",
            linestyle="dashed",
            linewidth=1,
        )
        plt.tight_layout()

    # plt.show()
    plt.figure(2)
    plt.suptitle(f"ROTI of medium substorms at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style, i)
        plt.hist(
            events_collection_ROTI[
                index_third:index_two_thirds, int((60 + times_of_interest[i]) / 5)
            ],
            bins=nr_bins,
            range=(0, 7),
        )
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0, 20)
        five_percentile = np.nanpercentile(
            events_collection_ROTI[index_third:index_two_thirds], 5, axis=0
        )
        nfive_percentile = np.nanpercentile(
            events_collection_ROTI[index_third:index_two_thirds], 95, axis=0
        )
        plt.axvline(
            five_percentile[int((60 + times_of_interest[i]) / 5)],
            color="red",
            linestyle="dashed",
            linewidth=1,
        )
        plt.axvline(
            nfive_percentile[int((60 + times_of_interest[i]) / 5)],
            color="green",
            linestyle="dashed",
            linewidth=1,
        )
        plt.tight_layout()

    # plt.show()
    plt.figure(3)
    plt.suptitle(f"ROTI of strong substorms at at {station} in 2018")
    for i in range(nr_plots):
        style_chooser(style, i)
        plt.hist(
            events_collection_ROTI[:index_third, int((60 + times_of_interest[i]) / 5)],
            bins=nr_bins,
            range=(0, 7),
        )
        plt.title(f"{times_of_interest[i]} min")
        plt.ylim(0, 20)
        five_percentile = np.nanpercentile(
            events_collection_ROTI[:index_third], 5, axis=0
        )
        nfive_percentile = np.nanpercentile(
            events_collection_ROTI[:index_third], 95, axis=0
        )
        plt.axvline(
            five_percentile[int((60 + times_of_interest[i]) / 5)],
            color="red",
            linestyle="dashed",
            linewidth=1,
        )
        plt.axvline(
            nfive_percentile[int((60 + times_of_interest[i]) / 5)],
            color="green",
            linestyle="dashed",
            linewidth=1,
        )
        plt.tight_layout()
    plt.show()

    if fancy_latex:
        plt.style.use("default")


def plot_histogram_event_GPS(
    events_collection_gps, time_gps_sorted, bins_sorted, GPS_events, fancy_latex=False
):

    borders = [
        bins_sorted[int((len(bins_sorted) - 1) / 3)],
        bins_sorted[int((len(bins_sorted) - 1) * 2 / 3)],
    ]

    index_third, index_two_thirds = int(len(events_collection_gps) / 3), int(
        len(events_collection_gps) * 2 / 3
    )
    station = "TRM"
    style = "downwards"
    times_of_interest = [-60, 0, 15, 16.5, 18, 30, 60, 120]
    xmin, xmax = 1e-4, 1e-2
    nr_bins = 50
    if fancy_latex:
        plt.style.use("../format_for_latex.mplstyle")
    nr_of_xticks = hour_area * 12 + 1
    index = int((16.2 + 60) / (4 * 3600) * 14401)
    median_event = np.nanmedian(events_collection_gps, axis=0)
    nfive_percentile = np.nanpercentile(events_collection_gps, 95, axis=0)
    five_percentile = np.nanpercentile(events_collection_gps, 5, axis=0)
    plt.plot(nfive_percentile, linewidth=3, color="green", label="95th percentile")
    plt.plot(five_percentile[::60], linewidth=3, color="red", label="5th percentile")
    plt.plot(median_event[::60], linewidth=3, color="black", label="median value")
    plt.axvline(index, color="black", linewidth=2)
    times_of_interest_temp = [-60, -30, 0, 12.6, 14.35, 15.0, 120, 150]
    for i in range(0, 8):
        print(times_of_interest_temp[i])
        index_temp = int((times_of_interest_temp[i] + 60) / (4 * 60) * 14401)
        plt.plot(
            index_temp, nfive_percentile[index_temp], "*", color="black", linewidth=10
        )
    print(nfive_percentile[index])
    plt.title(
        f"All recorded substorms by the gps receivers in {station} in 2018\n"
        + f"{GPS_events} substorms collected"
    )
    plt.xlabel("minutes")
    plt.ylabel("noise values from the NMEA [m]")
    plt.ylim(5e-5, 1)
    plt.legend()
    plt.yscale("log")
    plt.show()

    for i in range(0, 8):
        style_chooser(style, i)
        index = int((times_of_interest[i] + 60) / (4 * 60) * 14401)
        plt.hist(
            events_collection_gps[:, index],
            bins=np.logspace(np.log10(xmin), np.log10(xmax), nr_bins),
        )

        plt.title(f"{times_of_interest[i]} min ")
        plt.axvline(
            np.nanmedian(events_collection_gps, axis=0)[index],
            color="black",
            linestyle="dashed",
            linewidth=1,
        )
        print("percentiles", five_percentile[index], nfive_percentile[index])
        plt.axvline(
            five_percentile[index], color="red", linestyle="dashed", linewidth=1
        )
        plt.axvline(
            nfive_percentile[index], color="green", linestyle="dashed", linewidth=1
        )
        plt.ylim(0, 10)
        plt.xlim(xmin, xmax)
        plt.gca().set_xscale("log")
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
        with open(file_path, "rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        (
            dates_mag,
            location_long,
            location_lat,
            geographic_north,
            geographic_east,
            geographic_z,
            magnetic_north,
            magnetic_east,
            magnetic_z,
        ) = obj_mag.receiver_specific_data(station)

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/data_ssd/data"
    path_event = desktop_path + "/substorm_event_list_2018.csv"
    path_mag = desktop_path + "/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event, verbose=False)
    if save_ram_memory:
        file_path = "../../data_storage_arrays/TRM_Magnetometer_data.txt"
        with open(file_path, "rb") as file:
            dates_mag = np.load(file, allow_pickle=True)
            magnetic_north = np.load(file, allow_pickle=True)
    else:
        obj_mag.read_csv(path_mag, verbose=False)
        station = "TRO"
        (
            dates_mag,
            location_long,
            location_lat,
            geographic_north,
            geographic_east,
            geographic_z,
            magnetic_north,
            magnetic_east,
            magnetic_z,
        ) = obj_mag.receiver_specific_data(station)


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
dates_event = pd.to_datetime(dates_event, format="%Y-%m-%d %H:%M:%S")


Norway_time = time_UTC_event + 1
lat, mag_time, Norway_time, dates_event = filtering_to_Norway_night(
    lat, mag_time, Norway_time, dates_event, verbose=False
)
# raise Exception("hello there")

########################## gps noise  ##################################


def create_fake_noise():
    n = 50200
    time_axis_gps = np.zeros((365, n + 365)) * np.nan
    gps_noise = np.zeros((365, n + 365)) * np.nan
    for i in range(365):
        time_axis_gps[i, : n + i] = np.linspace(0, 24, n + i)
        gps_noise[i, : n + i] = np.ones(n + i) * (i + 1)
        print(gps_noise[i, :])
    return time_axis_gps, gps_noise


def statistical_reduction_of_data(gps_data, start_index, end_index):
    originial_shape = gps_data.shape
    print(originial_shape)
    gps_data = gps_data.flatten()
    median1 = np.nanmedian(gps_data[start_index:end_index])
    median2 = np.nanmedian(gps_data[:start_index])
    ratio = median1 / median2
    gps_data[start_index:end_index] = gps_data[start_index:end_index] / ratio
    gps_data = gps_data.reshape(originial_shape)
    return gps_data


def load_gps_noise():
    file_path = "../../data_storage_arrays/NMEA_data_TRM.txt"
    with open(file_path, "rb") as file:
        time = np.load(file)
        noise = np.load(file)
    start_index_weird_time = 7649115 - 50500
    end_index_weird_time = 7858915 - 50500
    noise = statistical_reduction_of_data(
        noise, start_index_weird_time, end_index_weird_time
    )
    return time, noise


time_axis_gps, gps_noise = load_gps_noise()

# time_axis_gps,gps_noise = run_NMEA_data(365,"TRM")
# time_axis_gps, gps_noise = create_fake_noise()

########################## ROTI  ##################################


def load_ROTI_data():
    file_path = "../../data_storage_arrays/TRO_ROTI_biint.txt"
    with open(file_path, "rb") as file:
        time = np.load(file)
        ROTI_biint = np.load(file)
    return time, ROTI_biint


time_ROTI_TRO, ROTI_biint_TRO = load_ROTI_data()


########################## creating bins ###################################
hour_area = 4
(
    bins_sorted,
    time_day_bins,
    time_of_event,
    mag_collection_sorted,
    ROTI_event_sorted,
    noise_gps_sorted,
    time_gps_sorted,
    mag_events,
    GPS_events,
) = create_bins_gps_ROTI_mag(
    hour_area,
    dates_mag,
    dates_event,
    Norway_time,
    magnetic_north,
    gps_noise,
    time_axis_gps,
    time_ROTI_TRO,
    ROTI_biint_TRO,
)


def clean_nans_gps_noise(time_gps_sorted, noise_gps_sorted):
    r = pd.date_range(start="2018-01-01T00:00:00", end="2018-01-01T04:00:00", freq="S")
    new_time = np.zeros((196, 4 * 60 * 60 + 1)) * np.nan
    new_gps_noise = np.zeros((196, 4 * 60 * 60 + 1)) * np.nan
    print(len(noise_gps_sorted[0, :]), len(noise_gps_sorted))
    for i in range(196):
        df = pd.DataFrame(r, columns=["time"])
        df["gps_noise"] = np.nan
        print(i * 100)
        for ii in range(36000):
            if not np.isnan(time_gps_sorted[i, ii]):
                index = round(time_gps_sorted[i, ii] * 3600)
                # print(index)
                # print(noise_gps_sorted[i,ii])
                # print("df before", df)
                df.gps_noise[index] = noise_gps_sorted[i, ii]
                # print("df after", df)

        # print(df["gps_noise"])
        new_time[i, :] = date_to_days(df["time"])
        new_gps_noise[i, :] = df["gps_noise"]
    file_path = "../../data_storage_arrays/filtered_NMEA_data_TRM.txt"
    with open(file_path, "wb") as file:
        np.save(file, new_time)
        np.save(file, new_gps_noise)


def load_cleaned_gps_noise():
    file_path = "../../data_storage_arrays/filtered_NMEA_data_TRM.txt"
    with open(file_path, "rb") as file:
        time = np.load(file)
        noise = np.load(file)
    start_index_weird_time = 7649115 - 50400
    end_index_weird_time = 7858915 - 50400
    print(noise)
    noise = statistical_reduction_of_data(
        noise, start_index_weird_time, end_index_weird_time
    )
    return time, noise


# clean_nans_gps_noise(time_gps_sorted,noise_gps_sorted)
new_time_gps, new_gps_noise = load_cleaned_gps_noise()
#########################plotting data#########################

# plot_histogram_event_mag(mag_collection_sorted,bins_sorted, mag_events, fancy_latex = False)
# plot_histogram_event_ROTI(ROTI_event_sorted,bins_sorted, mag_events, fancy_latex = False)
plot_histogram_event_GPS(
    new_gps_noise, new_time_gps, bins_sorted, GPS_events, fancy_latex=False
)
