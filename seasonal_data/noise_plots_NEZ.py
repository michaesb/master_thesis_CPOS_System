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
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plotting_noise_Z():
    plt.plot(noise_Z[:,0], label="21-03")
    plt.plot(noise_Z[:,1], label="3-9" )
    plt.plot(noise_Z[:,2], label="9-15")
    plt.plot(noise_Z[:,3], label="15-21")
    plt.title("Z-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/Z_coordinate_noise_"+\
                    receiver+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/Z_coordinate_noise_"+\
                    receiver+"_"+year)
    plt.show()

def plotting_noise_N():
    plt.plot(noise_N[:,0], label="21-03")
    plt.plot(noise_N[:,1], label="3-9" )
    plt.plot(noise_N[:,2], label="9-15")
    plt.plot(noise_N[:,3], label="15-21")
    plt.title("N-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/N_coordinate_noise_"+\
                    receiver+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/N_coordinate_noise_"+\
                    receiver+"_"+year)
    plt.show()

def plotting_noise_E():
    plt.plot(noise_E[:,0], label="21-03")
    plt.plot(noise_E[:,1], label="3-9" )
    plt.plot(noise_E[:,2], label="9-15")
    plt.plot(noise_E[:,3], label="15-21")
    plt.title("E-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/E_coordinate_noise_"+\
                    receiver+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/E_coordinate_noise_"+\
                    receiver+"_"+year)
    plt.show()

receiver_stations = ["SIM","HFS","STE","TRM","NAK", "STA","RAN","FOL"]
nr_days = 365
year = "2018"
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

noise_N = np.zeros((nr_days,4))
noise_E = np.zeros((nr_days,4))
noise_Z = np.zeros((nr_days,4))

for i in range(1,366):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

noise_stored = np.array([0.,0.,0.])
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
        sigma_Z = accuracy_NMEA(Z-np.median(Z))
        sigma_N = accuracy_NMEA(N-np.median(N))
        sigma_E = accuracy_NMEA(E-np.median(E))
        N_s = len(sigma_Z)
        index_3, index_9, index_15 ,index_21 = int(N_s/8.),int(N_s*3/8.),\
                                               int(N_s*5/8.),int(N_s*7/8.)
        if i==1:
            noise_N[i,0] = np.nan
            noise_E[i,0] = np.nan
            noise_Z[i,0] = np.nan
        else:
            noise_N[i,0] =np.nansum(np.concatenate([sigma_N[index_21:],noise_stored[0]]))
            noise_E[i,0] =np.nansum(np.concatenate([sigma_E[index_21:],noise_stored[1]]))
            noise_Z[i,0] =np.nansum(np.concatenate([sigma_Z[index_21:],noise_stored[2]]))

        noise_N[i,1], noise_E[i,1], noise_Z[i,1] = \
        np.nansum(sigma_N[index_3:index_9]), np.nansum(sigma_E[index_3:index_9]), np.nansum(sigma_Z[index_3:index_9])

        noise_N[i,2], noise_E[i,2], noise_Z[i,2] = \
        np.nansum(sigma_N[index_9:index_15]), np.nansum(sigma_E[index_9:index_15]), np.nansum(sigma_Z[index_9:index_15])

        noise_N[i,3], noise_E[i,3], noise_Z[i,3] = \
        np.nansum(sigma_N[index_15:index_21]), np.nansum(sigma_E[index_15:index_21]), np.nansum(sigma_Z[index_15:index_21]),

        noise_stored = sigma_N[index_21:], sigma_E[index_21:], sigma_Z[index_21:]

    # plot_datapoints()

    plotting_noise_N()
    plotting_noise_E()
    plotting_noise_Z()
