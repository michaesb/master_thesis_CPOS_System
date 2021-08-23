import numpy as np
import matplotlib.pyplot as plt

# from scipy.signal import savgol_filter
import sys, time

sys.path.insert(0, "..")
from tqdm import tqdm
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA_opt, filtering_outliers


def plotting_noise(date, noise):
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Okt",
        "Nov",
        "Des",
    ]
    plt.plot(date, noise[:, 1], "green", label="3-9")
    plt.plot(date, noise[:, 2], "blue", label="9-15")
    plt.plot(date, noise[:, 3], "black", label="15-21")
    plt.plot(
        date,
        noise[:, 0],
        "red",
        label="21-03",
    )
    plt.title("Z-coordinate noise at " + receiver + " over " + year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.xticks([4, 9, 14, 19, 24, 29])
    # plt.xticks(np.arange(0,len(date),30),months[:int(len(date)/30)])
    plt.legend()
    plt.show()


receiver = "TRM"
nr_days = 365
year = "2018"


def run_filter_plot_NMEA_data(nr_days, year, receiver):
    date = []
    noise = np.zeros((nr_days, 4))
    counter_first = 1
    for i in range(1, nr_days + 1):
        if len(str(i)) == 1:
            date.append("00" + str(i))
        elif len(str(i)) == 2:
            date.append("0" + str(i))
        else:
            date.append(str(i))

    for i in tqdm(range(len(date)), desc="RTIM data"):
        # for i in range(len(date)):
        # progress_bar(i,len(date))
        adress = (
            "/run/media/michaelsb/data_ssd/data/NMEA/"
            + year
            + "/"
            + date[i]
            + "/"
            + "NMEA_M"
            + receiver
            + "_"
            + date[i]
            + "0.log"
        )
        obj = ReadNMEAData()
        try:
            obj.read_textfile(adress, verbose=False)
            N, E, Z = obj.coordinates
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = (
                    "/scratch/michaesb/data/NMEA/"
                    + year
                    + "/"
                    + date[i]
                    + "/NMEA_M"
                    + receiver
                    + "_"
                    + date[i]
                    + "0.log"
                )
                obj = ReadNMEAData()
                obj.read_textfile(adress, verbose=False)
                N, E, Z = obj.coordinates
                Office_computer = 1
            except FileNotFoundError:
                tqdm.write(
                    "no " + receiver + " file here at day: " + str(i) + " year: " + year
                )
                tqdm.write(adress)
                noise[i, :] = np.nan
                continue

        if len(Z) < 60:
            noise[i, :] = np.nan
            continue

        sigma = accuracy_NMEA_opt(Z - np.mean(Z))
        index_3, index_9, index_15, index_21 = (
            int(len(sigma) / 8.0),
            int(len(sigma) * 3 / 8.0),
            int(len(sigma) * 5 / 8.0),
            int(len(sigma) * 7 / 8.0),
        )
        if counter_first == 1:
            noise[i, 0] = np.nan
            counter_first = 0
        else:
            noise[i, 0] = np.nanmean(np.concatenate([noise_stored, sigma[:index_3]]))
        noise[i, 1] = np.nanmean(sigma[index_3:index_9])
        noise[i, 2] = np.nanmean(sigma[index_9:index_15])
        noise[i, 3] = np.nanmean(sigma[index_15:index_21])
        noise_stored = sigma[index_21:]

    plotting_noise(date, noise)


run_filter_plot_NMEA_data(nr_days, year, receiver)
