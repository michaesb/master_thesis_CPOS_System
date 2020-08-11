import numpy as np
import matplotlib.pyplot as plt
import unittest, sys
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def plotting():
    plt.subplot(4, 1, 1)
    plt.plot(obj.time_h,N-ave_N)
    plt.title("coordinates")
    plt.ylabel("arcdegrees")
    plt.xticks([])

    plt.subplot(4,1,2)
    plt.plot(obj.time_h,E-ave_E)
    plt.ylabel("arcdegrees")
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
for i in receiver:
    adress_M = "/run/media/michaelsb/HDD Linux/data/NMEA/2015/076/NMEA_M"\
    +i+"_0760.log"
    obj = ReadNMEAData()
    obj.read_textfile(adress_M,verbose=False)
    #obj.display_GPS_indicator()
    # print(obj.day_year, "day_year")
    N, E, Z = obj.coordinates
    ave_N, ave_E, ave_Z = np.sum(N)/obj.nr_datapoints,\
    np.sum(E)/obj.nr_datapoints ,np.sum(Z)/obj.nr_datapoints
    print(ave_N, ave_E,"coordinates in ",i)
    #plotting()
