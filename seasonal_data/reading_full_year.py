import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def recording_data_2018(receiver):
    adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2018/"+date[i]+"/"+\
    "NMEA_M"+receiver +"_"+date[i]+"0.log"
    obj = ReadNMEAData()
    if receiver == "HFS":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        yeardataHFS_z[i,:len(Z)] = Z
    if receiver == "STE":
        obj.read_textfile(adress,verbose=False)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        yeardataSTE_z[i,:len(Z)] = Z
    if receiver == "TRM":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        yeardataTRM_z[i,:len(Z)] = Z


def plot_datapoints():
    plt.plot(datapoints_per_day)
    plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plot_coordinates():
    plt.plot(np.sum(yeardataHFS_z, axis=1)/obj.datapoints[0])
    plt.plot(np.sum(yeardataSTE_z, axis=1)/obj.datapoints[0])
    plt.plot(np.sum(yeardataTRM_z, axis=1)/obj.datapoints[0])
    plt.title("z-coordinate read at "+receiver+" over 2019")
    plt.ylabel("offset from average [m]")
    plt.xticks([])

days_in_a_month  = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

receiver_stations = ["HFS","STE","TRM"]
nr_days = 365
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []


yeardataHFS_z = np.zeros((nr_days,84600))
yeardataSTE_z = np.zeros((nr_days,84600))
yeardataTRM_z = np.zeros((nr_days,84600))


for i in range(1,366):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))
for receiver in receiver_stations:
    for i in range(len(date)):
        progress_bar(i,len(date))
        # recording_data_2018()
        try:
            recording_data_2018(receiver)
        except:
            pass
    plot_datapoints()
