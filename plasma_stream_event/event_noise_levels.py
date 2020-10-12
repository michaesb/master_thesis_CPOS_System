import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA_opt, filtering_outliers

office_computer = 0
home_computer = 0
laptop_computer = 0

def recording_data_2018():
    obj = ReadNMEAData()
    obj.read_textfile(adress,verbose=False)
    print(obj.day_year, receiver_stations[j])
    if receiver_stations[j] == "HFS":
        doy.append(str(obj.day_year))
    N,E,Z = obj.coordinates
    return N,E,Z

def plotting_noise(noise,title_part):
    for i in range(len(receiver_stations)):
        plt.plot(date,noise[:,i])
    plt.title("noise over "+year+ str(title_part))
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    # plt.xticks([i.split(" ")[:1] for i in doy])
    plt.legend(receiver_stations)
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/Z_coordinate_noise_event"+\
                     "all_stations_"+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/Z_coordinate_noise_event"+\
                     "all_stations_"+"_"+year)
    plt.show()

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
year = "2018"
date = ["148","149","150","151","152","153","154","156","157"]
doy = []
nr_days = len(date)

noise_Z = np.zeros((nr_days,len(receiver_stations)))*np.nan
noise_N = np.zeros((nr_days,len(receiver_stations)))*np.nan
noise_E = np.zeros((nr_days,len(receiver_stations)))*np.nan


for j in range(len(receiver_stations)):
    for i in range(len(date)):
        progress_bar(int(i+j*nr_days) ,nr_days*(1+len(receiver_stations)))
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver_stations[j] +"_"+date[i]+"0.log"

        try:
            N,E,Z = recording_data_2018()
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver_stations[j]+"_"+date[i]+"0.log"
                N,E,Z = recording_data_2018()
                Office_computer = 1
            except FileNotFoundError:
                try:
                    adress = "/home/michael/Documents/Data/NMEA/"+year+"/"+date[i]+"/NMEA_M"\
                    +receiver_stations[j]+"_"+date[i]+"0.log"
                    N,E,Z = recording_data_2018()
                    laptop_computer = 1

                except FileNotFoundError:
                    print("no "+receiver_stations[j]+" file here at day: " + str(i) +" year: "+year)
                    print(adress)
                    noise_Z[i,j] = np.nan
                    noise_N[i,j] = np.nan
                    noise_E[i,j] = np.nan
                    continue

        if len(Z) < 60:
            noise_Z[i,nr_stations] = np.nan
            noise_N[i,nr_stations] = np.nan
            noise_E[i,nr_stations] = np.nan
        else:
            sigma_Z = accuracy_NMEA_opt(Z-np.median(Z))
            noise_Z[i,j] = np.nanmedian(sigma_Z)
            sigma_N = accuracy_NMEA_opt(N-np.median(N))
            noise_N[i,j] = np.nanmedian(sigma_N)
            sigma_E = accuracy_NMEA_opt(E-np.median(E))
            noise_E[i,j] = np.nanmedian(sigma_E)
    # plot_datapoints()
plotting_noise(noise_N," coordinate N")
plotting_noise(noise_E," coordinate E")
plotting_noise(noise_Z," coordinate Z")
