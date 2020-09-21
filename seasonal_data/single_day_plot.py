import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from extra.error_calculation_NMA_standard import accuracy_NMEA, filtering_outliers
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def plotting_coordinates():
    plt.subplot(3,1,1)
    plt.plot(obj.time_h,obj.nr_satellites)
    plt.title("noise and # of sattelites for " +receiver+ " at day: "+date +" in "+year)
    plt.ylabel("number of sattelites")
    plt.xticks([])

    plt.subplot(3,1,2)
    plt.plot(obj.time_h, Z-np.mean(Z), "r*", label="unfiltered")
    plt.plot(t, Z_filtered-np.mean(Z_filtered), "b*",label="filtered")
    plt.ylabel("coordinate Z [m]")
    plt.legend()
    plt.xticks([])

    plt.subplot(3,1,3)
    plt.plot(t[30:-30],sigma_Z, label="before savoksy golay filter")
    plt.plot(t[30:-30],sigma_Z_smooth, label ="smoothed")
    plt.ylabel("noise (sample mean)")
    plt.xlabel("time of day [hours]")
    plt.legend()
    plt.show()


receiver_stations = ["HFS", "NAK","RAN", "SIM","STA", "STE", "TRM"]
date = "151"
year = "2018"

for receiver in receiver_stations:

    adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date+"/"+"NMEA_M"+receiver +"_"+date+"0.log"
    obj = ReadNMEAData()
    try:
        obj.read_textfile(adress,verbose=False,filter_4=True)

    except:
        try:
            adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2018/"+date+"/"+\
            "NMEA_M"+receiver +"_"+date+"0.log"
            obj.read_textfile(adress,verbose=False,filter_4=True)
        except:
            print("path not found")
            print(adress)
            continue
    obj.display_GPS_indicator()
    print(obj.day_year, "day_year")
    print(100*obj.datapoints[0]/obj.datapoints[1],"% datapoints gps fix")
    N, E, Z = obj.coordinates
    Z,Z_filtered,t = filtering_outliers(Z,verbose=True, t=obj.time_h)
    sigma_Z = accuracy_NMEA(Z_filtered-np.mean(Z_filtered))
    sigma_Z_smooth= savgol_filter(sigma_Z,window_length=(5*60+1),polyorder=3)
    plotting_coordinates()
