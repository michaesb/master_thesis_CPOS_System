import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA_opt, filtering_outliers

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
office_computer = 0
home_computer = 0

def recording_data_2018(receiver):
    obj = ReadNMEAData()
    obj.read_textfile(adress,verbose=False)
    datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
    N,E,Z = obj.coordinates
    return N,E,Z


def plot_datapoints():
    plt.plot(date,datapoints_per_day)
    plt.plot(date,datapoints_per_day,"*")
    plt.plot(date,dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plotting_noise_Z():
    plt.plot(date,noise_Z[:,1], "-g", label="3-9")
    plt.plot(date,noise_Z[:,2], "blue", label="9-15")
    plt.plot(date,noise_Z[:,3], "black", label="15-21" )
    plt.plot(date,noise_Z[:,0],"-r",label="21-03",)
    plt.title("Z-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xticks(np.linspace(0,11/12,12)*len(date),months)
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
    plt.plot(date,noise_N[:,1], "-g", label="3-9")
    plt.plot(date,noise_N[:,2], "blue", label="9-15")
    plt.plot(date,noise_N[:,3], "black", label="15-21" )
    plt.plot(date,noise_N[:,0],"-r",label="21-03",)
    plt.title("N-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xticks(np.linspace(0,11/12,12)*len(date),months)
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
    plt.plot(date,noise_E[:,1], "-g", label="3-9")
    plt.plot(date,noise_E[:,2], "blue", label="9-15")
    plt.plot(date,noise_E[:,3], "black", label="15-21" )
    plt.plot(date,noise_E[:,0],"-r",label="21-03",)
    plt.title("E-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.xticks(np.linspace(0,11/12,12)*len(date),months)
    plt.legend()
    if office_computer:
        plt.savefig("../../plot_master_thesis/auto_plots/E_coordinate_noise_"+\
                    receiver+"_"+year)
    if home_computer:
        plt.savefig("../../../Skrivebord/master_thesis_plots/auto_plots/E_coordinate_noise_"+\
                    receiver+"_"+year)
    plt.show()

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
nr_days = 365
year = "2018"
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

noise_N = np.zeros((nr_days,4))
noise_E = np.zeros((nr_days,4))
noise_Z = np.zeros((nr_days,4))

for i in range(1,nr_days+1):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

noise_stored = []
for receiver in receiver_stations:
    datapoints_per_day = np.zeros(nr_days)
    dataline_per_day = np.zeros(nr_days)
    for i in range(len(date)):
        progress_bar(i,len(date))
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"
        try:
            N,E,Z = recording_data_2018(receiver)
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver+"_"+date[i]+"0.log"
                N,E,Z = recording_data_2018(receiver)
                Office_computer = 1
            except FileNotFoundError:
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

        sigma_N = accuracy_NMEA_opt(N-np.mean(N))
        sigma_E = accuracy_NMEA_opt(E-np.mean(E))
        sigma_Z = accuracy_NMEA_opt(Z-np.mean(Z))
        index_3, index_9, index_15 ,index_21 = \
        int(len(sigma_Z)/8.),int(len(sigma_Z)*3/8.),int(len(sigma_Z)*5/8.),int(len(sigma_Z)*7/8.)
        if i==0:
            noise_N[i,0] = np.nan
            noise_E[i,0] = np.nan
            noise_Z[i,0] = np.nan
        else:
            noise_N[i,0] =np.nanmean(np.concatenate([noise_stored[0],sigma_N[:index_3]]))
            noise_E[i,0] =np.nanmean(np.concatenate([noise_stored[1],sigma_E[:index_3]]))
            noise_Z[i,0] =np.nanmean(np.concatenate([noise_stored[2],sigma_Z[:index_3]]))

        noise_N[i,1], noise_E[i,1], noise_Z[i,1] = \
        np.nanmean(sigma_N[index_3:index_9]), np.nanmean(sigma_E[index_3:index_9]), np.nanmean(sigma_Z[index_3:index_9])

        noise_N[i,2], noise_E[i,2], noise_Z[i,2] = \
        np.nanmean(sigma_N[index_9:index_15]), np.nanmean(sigma_E[index_9:index_15]), np.nanmean(sigma_Z[index_9:index_15])

        noise_N[i,3], noise_E[i,3], noise_Z[i,3] = \
        np.nanmean(sigma_N[index_15:index_21]), np.nanmean(sigma_E[index_15:index_21]), np.nanmean(sigma_Z[index_15:index_21]),

        noise_stored = [sigma_N[index_21:], sigma_E[index_21:], sigma_Z[index_21:]]

    # plot_datapoints()


    plotting_noise_N()
    plotting_noise_E()
    plotting_noise_Z()

"""
0.43563175201416016 :reading text files
0.0033118724822998047 :noise calculation
0.0007843971252441406 :mean and storing values
0.4397318363189697 :total time
"""
