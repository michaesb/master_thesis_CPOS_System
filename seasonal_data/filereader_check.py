import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def extract_points():
    obj.read_textfile(adress,verbose=False)
    N,E,Z = obj.coordinates
    pos_N[i,j] = np.mean(N)
    print(obj.day_year,i)



office_computer = 0
home_computer = 0

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
nr_days = 365
year = "2018"
date = []
pos_N = np.zeros((nr_days,len(receiver_stations)))


def plot_datapoints():
    for j in range(len(receiver_stations)):
        plt.plot(pos_N[:,j])
    plt.legend(receiver_stations)
    plt.ylabel("datapoints read with average N positions")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year over all receivers")
    plt.show()

for i in range(1,nr_days):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

for j in range(len(receiver_stations)):
    for i in range(len(date)):
        progress_bar(int(i+j*nr_days) ,nr_days*(1+len(receiver_stations)))
        try:
            adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
            "NMEA_M"+receiver_stations[j] +"_"+date[i]+"0.log"
            extract_points()
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver_stations[j]+"_"+date[i]+"0.log"
                extract_points()
                office_computer = 1
            except FileNotFoundError:
                # print("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                # print(adress)
                pos_N[i,j] = np.nan
                continue

plot_datapoints()
