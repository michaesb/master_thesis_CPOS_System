import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def plotting_track_4():
    divides = 20
    t = np.linspace(0,24,len(obj.qualities_indicator))

    for i in range(divides):
        fra, til = int(i*len(obj.track_4)/divides), int((i+1)*len(obj.track_4)/divides)
        plt.plot(t[fra:til],obj.track_4[fra:til],'*')
        plt.title("high resolution of the fix float change")
        plt.xlabel("time [h]")
        plt.ylabel("quality indicator")
        plt.show()

def plotting_coordinates():
    plt.subplot(4, 1, 1)
    plt.plot(obj.time_h,N-ave_N)
    plt.title("coordinates for " +receiver)
    plt.ylabel("distance[m]")
    plt.xticks([])

    plt.subplot(4,1,2)
    plt.plot(obj.time_h,E-ave_E)
    plt.ylabel("distance[m]")
    plt.xticks([])

    plt.subplot(4,1,3)
    plt.plot(obj.time_h, Z-ave_Z)
    plt.ylabel("distance[m]")
    plt.xticks([])

    plt.subplot(4,1,4)
    plt.plot(obj.time_h,obj.nr_satellites)
    plt.ylabel("number of sattelites")
    plt.xlabel("time of day [hours]")
    plt.show()

receiver_stations = ["HFS", "NAK","RAN", "SIM","STA", "STE", "TRM"]
date = "077"
year = "2015"
for receiver in receiver_stations:
    try:
        adress_M = "/home/michael/Documents/Data/NMEA/"+year+"/"+date+"/NMEA_M"\
        +receiver+"_"+date+"0.log"
        obj = ReadNMEAData()
        obj.read_textfile(adress_M,verbose=False,filter_4=True)
        obj.display_GPS_indicator()
        print(obj.day_year, "day_year")
        print(obj.datapoints, "number of datapoints (and lines)")
        print(obj.quality_indicator)
        N, E, Z = obj.coordinates
        ave_N, ave_E, ave_Z = np.sum(N)/obj.datapoints[0],\
        np.sum(E)/obj.datapoints[0] ,np.sum(Z)/obj.datapoints[0]
        print(obj.datapoints[0]/obj.datapoints[1],"percentage datapoints")
        print(ave_N, ave_E,"coordinates in ", receiver)
        # plotting_track_4()
        # plotting_qualities()
        plotting_coordinates()
        print(adress_M)
    except:
        print("no"+receiver+"file here at day: " + date +" year: "+year)
