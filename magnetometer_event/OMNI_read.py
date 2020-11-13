import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData

obj = ReadOMNIData()

try:
    path = "/scratch/michaesb/OMNI_HRO_1MIN_179769.csv"
    obj.read_csv(path, verbose = True)
except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/OMNI_HRO_1MIN_179769.csv"
    obj.read_csv(path, verbose = True)

B_z = obj.ACE_B_z
AE = obj.AE_index
t = obj.time
dates, year = obj.day_of_year
days = date_to_days(dates)
days_hour = days + t/24
plt.plot(range(len(days)),days)
plt.show()

plt.plot(range(len(days)), B_z)
plt.title("B_Z values")
plt.ylabel("magnetic values [nT]")
plt.xlabel("t [hours]")
plt.show()


plt.plot(range(len(days)), AE)
plt.title("AE values")
plt.ylabel("magnetic values [nT]")
plt.xlabel("t [hours]")
plt.show()
