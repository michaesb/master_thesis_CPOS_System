import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA, filtering_outliers

def recording_data_2018(receiver,n):
    if receiver == "HFS":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        if obj.datapoints[0]> 48000:
            n +=1
            yeardataHFS_z[i,:len(Z)] = Z
        else:
            print(obj.datapoints,"datapoints extra")
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
    if receiver == "SIM":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        yeardataSIM_z[i,:len(Z)] = Z
    return N,E,Z,n

def plot_datapoints():
    # plt.plot(datapoints_per_day)
    plt.plot(datapoints_per_day,"*")
    # plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plot_coordinates():
    print(z_n)
    HFS =np.sum(yeardataHFS_z,axis =1)
    ind_fil =np.nonzero(HFS)
    plt.plot(HFS[ind_fil])
    # plt.plot(np.sum(yeardataSTE_z, axis=1)/z_n)
    # plt.plot(np.sum(yeardataTRM_z, axis=1)/z_n)
    plt.title("z-coordinate read at "+receiver+" over 2019")
    plt.ylabel("offset from average [m]")
    plt.xticks([])
    plt.show()
    # plt.plot(noise_N,label= "N")
    # plt.plot(noise_E,label= "E")
    for i in range(3):
        for j in range(len(noise_Z[:,0])):
            if noise_Z[j,i]<3.03e+7:
                noise_Z[j,i] = np.nan


    plt.plot(noise_Z[np.nonzero(noise_Z)])
    plt.title("coordinates noise at "+receiver+" over 2019")
    plt.ylabel("sample mean [m]")
    plt.xlabel("days")
    # plt.plot(noise_Z[np.nonzero(noise_Z),1],label= "Z_6_12")
    # plt.title("coordinates noise at "+receiver+" over 2019")
    # plt.xlabel("days")
    # plt.ylabel("sample mean [m]")
    # plt.plot(noise_Z[np.nonzero(noise_Z),2],label= "Z_12_18")
    # plt.title("coordinates noise at "+receiver+" over 2019")
    # plt.xlabel("days")
    # plt.ylabel("sample mean [m]")
    # plt.plot(noise_Z[np.nonzero(noise_Z),3],label= "Z_18_24")
    # plt.title("coordinates noise at "+receiver+" over 2019")
    # plt.xlabel("days")
    # plt.ylabel("sample mean [m]")
    plt.show()
    # plt.xticks([])

days_in_a_month  = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

receiver_stations = ["HFS"] #["HFS","STE","TRM","SIM"]
nr_days = 365
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

yeardataHFS_z = np.zeros((nr_days,84600))
yeardataSTE_z = np.zeros((nr_days,84600))
yeardataTRM_z = np.zeros((nr_days,84600))
yeardataSIM_z = np.zeros((nr_days,84600))
noise_N = np.zeros((nr_days,4))
noise_E = np.zeros((nr_days,4))
noise_Z = np.zeros((nr_days,4))


for i in range(1,366):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

for receiver in receiver_stations:
    n_n = 0
    e_n = 0
    z_n = 0
    for i in range(len(date)):
        progress_bar(i,len(date))
        # recording_data_2018()
        N,E,Z = np.zeros((1)),np.zeros((1)), np.zeros((1)),
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2018/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"
        obj = ReadNMEAData()
        try:
            N,E,Z,z_n= recording_data_2018(receiver,z_n)
            # pass
        except:

            pass
        n = len(N)
        noise_N[i,0], noise_N[i,1], noise_N[i,2], noise_N[i,3] = \
        np.mean(accuracy_NMEA(N[:int(n/4)])), np.mean(accuracy_NMEA(N[int(n/4):int(n/2)])),\
        np.mean(accuracy_NMEA(N[int(n/2):3*int(n/4)])),np.mean(accuracy_NMEA(N[3*int(n/4):]))
        noise_E[i,0], noise_E[i,1], noise_E[i,2], noise_E[i,3] = \
        np.mean(accuracy_NMEA(E[:int(n/4)])), np.mean(accuracy_NMEA(E[int(n/4):int(n/2)])),\
        np.mean(accuracy_NMEA(E[int(n/2):3*int(n/4)])),np.mean(accuracy_NMEA(E[3*int(n/4):]))
        noise_Z[i,0], noise_Z[i,1], noise_Z[i,2], noise_Z[i,3] = \
        np.mean(accuracy_NMEA(Z[:int(n/4)])), np.mean(accuracy_NMEA(Z[int(n/4):int(n/2)])),\
        np.mean(accuracy_NMEA(Z[int(n/2):3*int(n/4)])),np.mean(accuracy_NMEA(Z[3*int(n/4):]))
    plot_datapoints()
    plot_coordinates()
