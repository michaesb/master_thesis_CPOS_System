import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from extra.error_calculation_NMA_standard import accuracy_NMEA
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData


def filtering_outliers(z):
    N = len(z)
    interval = 60
    z_copy = z.copy()
    for i in range(0,len(z),interval):
        ave_z = np.mean(z_copy[i:i+interval])
        z_60 = abs(z_copy[i:i+interval]-ave_z)
        z_temp = np.where( z_60 > 0.2,np.nan,z_copy[i:i+interval])
        z_temp = np.where( z_60 > 3*np.std(z_60), np.nan,z_temp)
        z_copy[i:i+interval] = z_temp
    z_resized = z_copy[np.logical_not(np.isnan(z_copy))]

    print(N,len(z_resized), "size of array", "percentage=", 100*len(z_resized)/N)
    return z, z_resized

def plotting_coordinates():

    ave_N, ave_E, ave_Z = np.mean(N),np.mean(E),np.mean(Z)
    t_filtered = np.linspace(0,24,len(Z_filtered))

    plt.subplot(3,1,1)
    plt.plot(obj.time_h,obj.nr_satellites)
    plt.title("noise and # of sattelites for " +receiver+ " at day: "+date +" in "+year)
    plt.ylabel("number of sattelites")
    plt.xticks([])

    plt.subplot(3,1,2)
    plt.plot(obj.time_h, Z-ave_Z, "r*", label="unfiltered")
    plt.plot(t_filtered, Z_filtered-np.mean(Z_filtered), "b*",label="filtered")
    plt.ylabel("coordinate Z [m]")
    plt.legend()
    plt.xticks([])

    plt.subplot(3,1,3)
    plt.plot(t_filtered[::60],sigma_Z, label="before savoksy golay filter")
    plt.plot(t_filtered[::60],sigma_Z_smooth, label ="smoothed")
    plt.ylabel("noise (sample mean)")
    plt.xlabel("time of day [hours]")
    plt.legend()
    plt.show()

receiver_stations = ["HFS", "NAK","RAN", "SIM","STA", "STE", "TRM"]
date = "076"
year = "2015"
for receiver in receiver_stations:
    try:
        adress_M = "/home/michael/Documents/Data/NMEA/"+year+"/"+date+"/NMEA_M"\
        +receiver+"_"+date+"0.log"
        obj = ReadNMEAData()
        obj.read_textfile(adress_M,verbose=False,filter_4=True)
    except:
        print("no"+receiver+"file here at day: " + date +" year: "+year)
        print(adress_M)

    obj.display_GPS_indicator()
    print(obj.day_year, "day_year")
    N, E, Z = obj.coordinates
    print(obj.datapoints[0]/obj.datapoints[1],"percentage datapoints")
    Z,Z_filtered = filtering_outliers(Z)
    sigma_Z = accuracy_NMEA(Z_filtered-np.mean(Z_filtered))
    sigma_Z_smooth= savgol_filter(sigma_Z,window_length=(5*60+1),polyorder=3)
    plotting_coordinates()
