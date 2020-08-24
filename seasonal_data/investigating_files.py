import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

receiver_stations = ["HFS","STE", "TRM"]
# receiver = receiver_stations[5]

adress_test = "/run/media/michaelsb/HDD Linux/data/NMEA/2019/001"

datapoints_per_day= np.zeros(365)
dataline_per_day= np.zeros(365)

date = []

yeardataHFS = np.zeros((365,3,84600))

for i in range(1,365):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))
for receiver in receiver_stations:
    for i in range(len(date)):
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2019/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"
        obj = ReadNMEAData()
        obj.read_textfile(adress,verbose=False,)
        print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        print(np.sum(Z)/obj.datapoints[0])

    plt.plot(datapoints_per_day)
    plt.plot(dataline_per_day)
    plt.title("datapoints read at "+receiver+" over 2019")
    plt.legend(["gps fix","other point"])
    plt.xlabel("time [months]")
    plt.ylabel("datapoints /lines ")
    plt.show()
