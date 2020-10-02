import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA, filtering_outliers

office_computer = 0
home_computer = 0

def recording_data_2018(receiver):
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
nr_days = 25
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
for receiver in receiver_stations:
    datapoints_per_day = np.zeros(nr_days)
    dataline_per_day = np.zeros(nr_days)
    for i in range(len(date)):
        progress_bar(i,len(date))
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"

        try:
            N,E,Z,t = recording_data_2018(receiver)
            home_computer = 1
        except:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver+"_"+date[i]+"0.log"
                N,E,Z,t = recording_data_2018(receiver)
                Office_computer = 1
            except:
                print("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                print(adress)
                noise_Z[i,nr_stations] = np.nan
                noise_N[i,nr_stations] = np.nan
                noise_E[i,nr_stations] = np.nan
                continue

        # N,N_filtered = filtering_outliers(N,verbose=False)
        # E,E_filtered = filtering_outliers(E,verbose=False)
        # Z,Z_filtered = filtering_outliers(Z,verbose=False)
        if len(Z) < 60:
            noise_Z[i,nr_stations] = np.nan
        else:
            sigma = accuracy_NMEA(Z-np.median(Z))
            # sigma = savgol_filter(sigma,window_length=(5*60+1),polyorder=3)
            noise_Z[i,nr_stations] = np.nanmedian(sigma)

        if len(N) < 60:
            noise_N[i,nr_stations] = np.nan
        else:
            sigma = accuracy_NMEA(N-np.median(N))
            # sigma = savgol_filter(sigma,window_length=(5*60+1),polyorder=3)
            noise_N[i,nr_stations] = np.nanmedian(sigma)

        if len(E) < 60:
            noise_E[i,nr_stations] = np.nan
        else:
            sigma = accuracy_NMEA(E-np.median(E))
            # sigma = savgol_filter(sigma,window_length=(5*60+1),polyorder=3)
            noise_E[i,nr_stations] = np.nanmedian(sigma)
    print(nr_stations, len(receiver_stations))
    nr_stations += 1
    # plot_datapoints()
plotting_noise(noise_N," coordinate N")
plotting_noise(noise_E," coordinate E")
plotting_noise(noise_Z," coordinate Z")
