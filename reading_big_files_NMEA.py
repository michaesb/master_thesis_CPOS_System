import numpy as np
import matplotlib.pyplot as plt
import unittest, sys
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

adress_MTRM = "/run/media/michaelsb/HDD Linux/data/NMEA/2015/076/NMEA_MTRM_0760.log"
obj = ReadNMEAData()
obj.read_textfile(adress_MTRM,verbose=True)
print(obj.day_year, "day_year")
print(obj.time_period, "time")
print(obj.horizontal_dil_of_pos, "dil of pos")

N, E, Z = obj.coordinates

plt.subplot(4, 1, 1)
plt.plot(obj.time_h,N-np.sum(N)/obj.datapoints)
plt.title("coordinates")
plt.ylabel("arcdegrees")
plt.xticks([])

plt.subplot(4,1,2)
plt.plot(obj.time_h,E-np.sum(E)/obj.datapoints)
plt.ylabel("arcdegrees")
plt.xticks([])

plt.subplot(4,1,3)
plt.plot(obj.time_h, Z-np.sum(Z)/obj.datapoints)
plt.ylabel("offset from average [m]")
plt.xticks([])

plt.subplot(4,1,4)
plt.plot(obj.nr_sattelite)
plt.ylabel("number of sattelites")
plt.xlabel("time of day [hours]")
plt.show()
