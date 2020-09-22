import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys, time
sys.path.insert(0, "..")
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA, filtering_outliers

def recording_data_2018(receiver):

    obj = ReadNMEAData()
    if receiver == "HFS":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        t = obj.time_h

    if receiver == "STE":
        obj.read_textfile(adress,verbose=False)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        t = obj.time_h
    if receiver == "TRM":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        t = obj.time_h
    return N,E,Z,t


def plot_datapoints():
    plt.plot(datapoints_per_day)
    plt.plot(datapoints_per_day,"*")
    plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plotting_noise():
    plt.plot(noise_Z_3_9, label="3-9" )
    plt.plot(noise_Z_9_15, label="9-15")
    plt.plot(noise_Z_15_21, label="15-21")
    plt.plot(noise_Z_21_03, label="21-03")
    plt.title("z-coordinate noise at "+receiver+" over "+year)
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    plt.show()

receiver_stations = ["HFS","STE","TRM"]
nr_days = 365
year = "2018"
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

noise = np.zeros((nr_days))
noise_Z_21_03 = np.zeros(nr_days)
noise_Z_3_9 = np.zeros(nr_days)
noise_Z_9_15 = np.zeros(nr_days)
noise_Z_15_21 = np.zeros(nr_days)

for i in range(1,366):
    if len(str(i))==1:
        date.append("00"+str(i))
    elif len(str(i))==2:
        date.append("0"+str(i))
    else:
        date.append(str(i))

Z_stored = np.array([0])
for receiver in receiver_stations:
    for i in range(len(date)):
        progress_bar(i,len(date))

        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"

        try: #1
            N,E,Z,t = recording_data_2018(receiver)
        except:
            try: #2
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver+"_"+date[i]+"0.log"
                N,E,Z,t = recording_data_2018(receiver)
            except:
                print("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                print(adress)
                noise_Z_3_9[i] = np.nan
                noise_Z_9_15[i] = np.nan
                noise_Z_15_21[i] = np.nan
                noise_Z_21_03[i] = np.nan
                continue

        Z,Z_filtered = filtering_outliers(Z,verbose=False)
        if len(Z_filtered) < 60:
            noise_Z_3_9[i] = np.nan
            noise_Z_9_15[i] = np.nan
            noise_Z_15_21[i] = np.nan
            noise_Z_21_03[i] = np.nan
            continue
        sigma = accuracy_NMEA(Z_filtered-np.median(Z_filtered))
        sigma = savgol_filter(sigma,window_length=(5*60+1),polyorder=3)
        N_s = len(sigma)
        if i==1 or i==len(date)-1:
            noise_Z_21_03[i] = np.nan
        else:
            noise_Z_21_03[i] =np.nanmedian(np.concatenate([sigma[int(N_s*7/8):],Z_stored]))
        noise_Z_3_9[i] = np.nanmedian(sigma[int(N_s/8):int(N_s*3/8)])
        noise_Z_9_15[i] = np.nanmedian(sigma[int(N_s*3/8):int(N_s*5/8)])
        noise_Z_15_21[i] = np.nanmedian(sigma[int(N_s*5/8):int(N_s*7/8)])
        Z_stored = sigma[int(N_s*7/8):]

    plot_datapoints()
    plotting_noise()
