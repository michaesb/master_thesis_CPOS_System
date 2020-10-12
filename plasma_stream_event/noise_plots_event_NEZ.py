import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA_opt, filtering_outliers


office_computer = 0
home_computer = 0
laptop_computer = 0

def recording_data_2018(receiver):
    obj = ReadNMEAData()
    obj.read_textfile(adress,verbose=False)
    N,E,Z = obj.coordinates
    return N,E,Z

def plotting_noise_Z():
    for i in range(day_res):
        plt.plot(date,noise_Z[:,i],"-*",label=str(24/day_res*i)+" - "+str(24/day_res*(i+1)))
    plt.title("Z-coordinate noise at "+receiver_stations[j]+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/Z_coordinate_noise_"+\
                    receiver_stations[j]+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/Z_coordinate_noise_"+\
                    receiver_stations[j]+"_"+year)
    plt.show()

def plotting_noise_N():
    for i in range(day_res):
        plt.plot(date,noise_N[:,i], label=str(24/day_res *i)+" - "+str(24/day_res *(i+1)))

    plt.title("N-coordinate noise at "+receiver_stations[j]+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/N_coordinate_noise_"+\
                    receiver_stations[j]+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/N_coordinate_noise_"+\
                    receiver_stations[j]+"_"+year)
    plt.show()

def plotting_noise_E():
    for i in range(day_res):
        plt.plot(date,noise_E[:,i],label=str(24/day_res*i)+" - "+str(24/day_res*(i+1)))

    plt.title("E-coordinate noise at "+receiver_stations[j]+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/E_coordinate_noise_event"+\
                    receiver_stations[j]+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/E_coordinate_noise_event"+\
                    receiver_stations[j]+"_"+year)
    plt.show()

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
year = "2018"
date = ["148","149","150","151","152","153","154","156","157"]
nr_days = len(date)

day_res = 8

noise_N = np.zeros((nr_days,day_res))
noise_E = np.zeros((nr_days,day_res))
noise_Z = np.zeros((nr_days,day_res))

noise_stored = []
for j in range(len(receiver_stations)):
    for i in range(len(date)):
        progress_bar(i,len(date))
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver_stations[j] +"_"+date[i]+"0.log"
        try:
            N,E,Z = recording_data_2018(receiver_stations[j])
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver_stations[j]+"_"+date[i]+"0.log"
                N,E,Z = recording_data_2018(receiver_stations[j])
                Office_computer = 1
            except FileNotFoundError:
                try:
                    adress = "/home/michael/Documents/Data/NMEA/"+year+"/"+date[i]+"/NMEA_M"\
                    +receiver_stations[j]+"_"+date[i]+"0.log"
                    N,E,Z = recording_data_2018(receiver_stations[j])
                    laptop_computer = 1
                except FileNotFoundError:
                    print("no "+receiver_stations[j]+" file here at day: " + str(i) +" year: "+year)
                    print(adress)
                    noise_N[i,:] = np.nan
                    noise_E[i,:] = np.nan
                    noise_Z[i,:] = np.nan
                    continue

        # Z,Z_filtered = filtering_outliers(Z,verbose=False)
        if len(Z) < 60:
            noise_N[i,:] = np.nan
            noise_E[i,:] = np.nan
            noise_Z[i,:] = np.nan
            continue

        sigma_N = accuracy_NMEA_opt(N-np.mean(N))
        sigma_E = accuracy_NMEA_opt(E-np.mean(E))
        sigma_Z = accuracy_NMEA_opt(Z-np.mean(Z))
        for k in range(day_res):
            ind_0, ind_1 = int(len(sigma_Z)*k/day_res),int(len(sigma_Z)*(k+1)/day_res)
            noise_N[i,k], noise_E[i,k], noise_Z[i,k] = \
            np.nanmean(sigma_N[ind_0:ind_1]), \
            np.nanmean(sigma_E[ind_0:ind_1]), \
            np.nanmean(sigma_Z[ind_0:ind_1])

    # plotting_noise_N()
    # plotting_noise_E()
    plotting_noise_Z()
