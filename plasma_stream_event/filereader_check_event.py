import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData

def extract_points():
    with open(adress, 'r') as infile:
        counter = 1
        for line in infile:
            if counter:
                counter = 0
            data = line.split(" ")[5]
            try:
                pos_N[i,j] = float(data.split(",")[2][:2])\
                        + float(data.split(",")[2][3:])/60
                break
            except ValueError:
                continue



office_computer = 0
home_computer = 0
laptop_computer = 0

receiver_stations = ["HFS","STE","TRM","NAK", "STA","RAN","FOL","SIM"]
nr_days = 365
start_date = 148
end_date = 155
year = "2018"
date = ["148","149","150","151","152","153","154","155"]
pos_N = np.zeros((nr_days,len(receiver_stations)))*np.nan

def plot_datapoints():
    for j in range(len(receiver_stations)):
        plt.plot(pos_N[:,j],'*')
    plt.legend(receiver_stations)
    plt.ylabel("datapoints read with average N positions")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year over all receivers")
    plt.show()


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
                try:
                    adress = "/home/michael/Documents/Data/NMEA/"+year+"/"+date[i]+"/NMEA_M"\
                    +receiver_stations[j]+"_"+date[i]+"0.log"
                    extract_points()
                    laptop_computer = 1
                except FileNotFoundError:
                    pos_N[i,j] = np.nan
                    continue

plot_datapoints()
