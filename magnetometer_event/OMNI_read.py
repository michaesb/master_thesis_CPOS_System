import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

obj = ReadOMNIData()

try:
    path = "/scratch/michaesb/OMNI_HRO_1MIN_179769.csv"
    obj.read_csv(path, verbose = True)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/OMNI_HRO_1MIN_179769.csv"
    obj.read_csv(path, verbose = True)

B_z = obj.ACE_B_z
AE = obj.AE_index
t = obj.time
dates, year = obj.day_of_year
days = date_to_days(dates)
days_hour = days + t/24.

B_z_positive = B_z[B_z>0]
B_z_negative = B_z[B_z<0]

plt.subplot(2,1,1)
plt.plot(days_hour[B_z>0], B_z_positive,"r", linewidth =0.4)
plt.plot(days_hour[B_z<0], B_z_negative, "g")
plt.plot(days_hour, np.zeros_like(days_hour), "r", linewidth=0.4)
plt.title("B_Z values and AE-index over 2018")
plt.ylabel("magnetic values [nT]")

plt.subplot(2,1,2)
plt.plot(days_hour, AE)
#plt.title(" over 2018")
plt.ylabel("magnetic values [nT]")
plt.xlabel("t [days]")
plt.axis([-15, 366, 0, 1600])
plt.show()
