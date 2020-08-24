import numpy as np
import matplotlib.pyplot as plt
import unittest, sys
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def plotting(t,N,E,Z,nr_satellites):
    plt.subplot(4, 1, 1)
    plt.plot(t,N)
    plt.title("coordinates")
    plt.ylabel("arcdegrees")
    plt.xticks([])

    plt.subplot(4,1,2)
    plt.plot(t,E)
    plt.ylabel("arcdegrees")
    plt.xticks([])

    plt.subplot(4,1,3)
    plt.plot(t, Z)
    plt.ylabel("offset from average [m]")
    plt.xticks([])

    plt.subplot(4,1,4)
    plt.plot(t,nr_satellites)
    plt.ylabel("number of sattelites")
    plt.xlabel("time of day [hours]")
    plt.show()

receiver = ["HFS", "NAK","RAN", "SIM","STA", "STE", "TRM"]
date = "076"

for j in range():
    for i in receiver:
        adress_M = "/run/media/michaelsb/HDD Linux/data/NMEA/2015/"+date+"/NMEA_M"\
        +i+"_"+date+"0.log"
        obj = ReadNMEAData()
        obj.read_textfile(adress_M,verbose=False)
        obj.display_GPS_indicator()
        print(obj.day_year, "day_year")
        print(obj.datapoints_line, "number of datapoints (and lines)")
        # print(obj.quality_indicator)
        N, E, Z = obj.coordinates
        ave_N, ave_E, ave_Z = np.sum(N)/obj.nr_datapoints,\
        np.sum(E)/obj.nr_datapoints ,np.sum(Z)/obj.nr_datapoints
        print(ave_N, ave_E,"coordinates in ",i)
        plotting(obj.time_h,N-ave_N,E-ave_E,Z-ave_Z,obj.nr_satellite)
