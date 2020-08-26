import numpy as np
import matplotlib.pyplot as plt
import unittest, sys
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def plotting():
    plt.subplot(4, 1, 1)
    plt.plot(obj.time_h,N-ave_N)
    plt.title("coordinates")
    plt.ylabel("distance [m]")
    plt.xticks([])

    plt.subplot(4,1,2)
    plt.plot(obj.time_h,E-ave_E)
    plt.ylabel("distance [m]")
    plt.xticks([])

    plt.subplot(4,1,3)
    plt.plot(obj.time_h, Z-ave_Z)
    plt.ylabel("offset from average [m]")
    plt.xticks([])

    plt.subplot(4,1,4)
    plt.plot(obj.time_h,obj.nr_satellites)
    plt.ylabel("number of sattelites")
    plt.xlabel("time of day [hours]")
    plt.show()

receiver = ["HFS", "NAK","RAN", "SIM","STA", "STE", "TRM"]
date = "157"

for i in receiver:
    adress_M = "/run/media/michaelsb/HDD Linux/data/NMEA/2019/"+date+"/NMEA_M"\
    +i+"_"+date+"0.log"
    obj = ReadNMEAData()
    obj.read_textfile(adress_M,verbose=False,filter_4=False)
    obj.display_GPS_indicator()
    print(obj.day_year, "day_year")
    print(obj.datapoints, "number of datapoints (and lines)")
    print(obj.quality_indicator)
    N, E, Z = obj.coordinates
    ave_N, ave_E, ave_Z = np.sum(N)/obj.datapoints[0],\
    np.sum(E)/obj.datapoints[0] ,np.sum(Z)/obj.datapoints[0]
    print(ave_N, ave_E,"coordinates in ", i)
    plotting()
