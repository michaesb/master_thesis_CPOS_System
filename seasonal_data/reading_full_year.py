import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

receiver_stations = ["HFS","STE","TRM"]
nr_days =365
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

def plotting_track_4():
    print(sum(obj.track_4)/obj.datapoints[1],"track 4")
    divides = 1
    for i in range(divides):
        fra, til = int(i*len(obj.track_4)/divides), int((i+1)*len(obj.track_4)/divides)
        plt.plot(obj.track_4[fra:til],'*')
        plt.title
        plt.show()

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
        progress_bar(i,len(date), ending="\n")
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2019/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"
        obj = ReadNMEAData()
        obj.read_textfile(adress,verbose=False)
        print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        if receiver == "HFS":
            print(np.sum(Z)/obj.datapoints[0], "HFS")
            yeardataHFS_z[i,:len(Z)] = Z
        if receiver == "STE":
            print(np.sum(Z)/obj.datapoints[0], "STE")
            yeardataSTE_z[i,:len(Z)] = Z
        if receiver == "TRM":
            print(np.sum(Z)/obj.datapoints[0], "TRM")
            yeardataTRM_z[i,:len(Z)] = Z

        # plotting_track_4()

    plt.subplot(2, 1, 1)
    if receiver == "HFS":
        plt.plot(np.sum(yeardataHFS_z, axis=1)/obj.datapoints[0])
    if receiver == "STE":
        plt.plot(np.sum(yeardataSTE_z, axis=1)/obj.datapoints[0])
    if receiver == "TRM":
        plt.plot(np.sum(yeardataTRM_z, axis=1)/obj.datapoints[0])
    plt.title("datapoints and z-coordinate read at "+receiver+" over 2019")
    plt.ylabel("offset from average [m]")
    plt.xticks([])

    plt.subplot(2,1,2)
    plt.plot(datapoints_per_day)
    plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.show()
