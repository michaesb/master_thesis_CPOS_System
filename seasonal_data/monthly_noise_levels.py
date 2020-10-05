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

def recording_data_2018():
    obj = ReadNMEAData()
    obj.read_textfile(adress,verbose=False)
    #print(obj.day_year, receiver)
    datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
    N,E,Z = obj.coordinates
    t = obj.time_h
    return N,E,Z,t


def plot_datapoints():
    plt.plot(datapoints_per_day)
    plt.plot(datapoints_per_day,"*")
    plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints/lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plotting_noise(noise,title_part):
    for i in range(nr_stations):
        plt.plot(noise[:,i])
    plt.title("noise over "+year+ str(title_part))
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend(receiver_stations)
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/Z_coordinate_noise_"+\
                    receiver+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/Z_coordinate_noise_"+\
                    receiver+"_"+year)
    plt.show()

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
nr_days = 365
year = "2018"
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

noise_Z = np.zeros((nr_days,len(receiver_stations)))
noise_N = np.zeros((nr_days,len(receiver_stations)))
noise_E = np.zeros((nr_days,len(receiver_stations)))

date = []

for i in range(1,nr_days):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

nr_stations = 0
for j in range(len(receiver_stations)):
    datapoints_per_day = np.zeros(nr_days)
    dataline_per_day = np.zeros(nr_days)
    for i in range(len(date)):
        progress_bar(int(i+j*nr_days) ,nr_days*(1+len(receiver_stations)))
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver_stations[j] +"_"+date[i]+"0.log"

        try:
            N,E,Z,t = recording_data_2018()
            home_computer = 1
        except:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver_stations[j]+"_"+date[i]+"0.log"
                N,E,Z,t = recording_data_2018()
                Office_computer = 1
            except:
                # print("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                # print(adress)
                noise_Z[i,nr_stations] = np.nan
                noise_N[i,nr_stations] = np.nan
                noise_E[i,nr_stations] = np.nan
                continue

        if len(Z) < 60:
            noise_Z[i,nr_stations] = np.nan
            noise_N[i,nr_stations] = np.nan
            noise_E[i,nr_stations] = np.nan
        else:
            sigma_Z = accuracy_NMEA_opt(Z-np.median(Z))
            noise_Z[i,nr_stations] = np.nanmedian(sigma_Z)
            sigma_N = accuracy_NMEA_opt(N-np.median(N))
            noise_N[i,nr_stations] = np.nanmedian(sigma_N)
            sigma_E = accuracy_NMEA_opt(E-np.median(E))
            noise_E[i,nr_stations] = np.nanmedian(sigma_E)
    # plot_datapoints()
plotting_noise(noise_N," coordinate N")
plotting_noise(noise_E," coordinate E")
plotting_noise(noise_Z," coordinate Z")
