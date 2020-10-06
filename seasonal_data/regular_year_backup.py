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
        z_n = obj.datapoints[0]
        yeardataHFS_z[i,:len(Z)] = Z

    if receiver == "STE":
        obj.read_textfile(adress,verbose=False)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        z_n = obj.datapoints[0]
        yeardataSTE_z[i,:len(Z)] = Z
    if receiver == "TRM":
        obj.read_textfile(adress,verbose=False)
        #print(obj.day_year, receiver)
        datapoints_per_day[i], dataline_per_day[i] = obj.datapoints
        N,E,Z = obj.coordinates
        z_n = obj.datapoints
        yeardataTRM_z[i,:len(Z)] = Z
    return N,E,Z,z_n


def plot_datapoints():
    plt.plot(datapoints_per_day)
    plt.plot(datapoints_per_day,"*")
    plt.plot(dataline_per_day)
    plt.legend(["gps fix","other point"])
    plt.ylabel("datapoints /lines ")
    plt.xlabel("time [days*-]")
    plt.title("datapoints over a full year at "+receiver)
    plt.show()

def plot_coordinates():
    plt.plot(np.median(yeardataHFS_z, axis=1))
    plt.plot(np.median(yeardataSTE_z, axis=1))
    plt.plot(np.median(yeardataTRM_z, axis=1))
    plt.title("z-coordinate read at "+receiver+" over 2018")
    plt.ylabel("offset from average [m]")

    plt.show()

def plotting_noise():
    plt.plot(noise_Z_6, label="0-6" )
    plt.plot(noise_Z_12, label="6-12")
    plt.plot(noise_Z_18, label="12-18")
    plt.plot(noise_Z_24, label="18-24")
    plt.title("z-coordinate noise at "+receiver+" over 2018")
    plt.ylabel("sample noise [m]")
    plt.xlabel("days")
    plt.legend()
    plt.show()

days_in_a_month  = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

receiver_stations = ["HFS","STE","TRM"]
nr_days = 365
year = "2018"
datapoints_per_day= np.zeros(nr_days)
dataline_per_day= np.zeros(nr_days)

date = []

yeardataHFS_z = np.zeros((nr_days,84600))
yeardataSTE_z = np.zeros((nr_days,84600))
yeardataTRM_z = np.zeros((nr_days,84600))

noise = np.zeros((nr_days))
noise_Z_6 = np.zeros(nr_days)
noise_Z_12 = np.zeros(nr_days)
noise_Z_18 = np.zeros(nr_days)
noise_Z_24 = np.zeros(nr_days)

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
        #adress = "/run/media/michaelsb/HDD Linux/data/NMEA/2018/"+date[i]+"/"+\
        #NMEA_M"+receiver +"_"+date[i]+"0.log"
        adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"\
         +receiver+"_"+date[i]+"0.log"
        try:
            N,E,Z,z_n = recording_data_2018(receiver)
            # Z,Z_filtered = filtering_outliers(Z)
            # sigma_Z = accuracy_NMEA(Z_filtered-np.median(Z_filtered))
            # sigma_Z_smooth= savgol_filter(sigma_Z,window_length=(5),polyorder=3)
            # noise_Z_6[i] = np.median(sigma_Z_smooth[:int(len(sigma_Z_smooth)/4)])
            # noise_Z_12[i] =np.median(sigma_Z_smooth[int(len(sigma_Z_smooth)/4):int(len(sigma_Z_smooth)/2)])
            # noise_Z_18[i] = np.median(sigma_Z_smooth[int(len(sigma_Z_smooth)/2):int(3*len(sigma_Z_smooth)/4)])
            # noise_Z_24[i] =np.median(sigma_Z_smooth[int(3*len(sigma_Z_smooth)/4):])
        except FileNotFoundError:
            print("no"+receiver+"file here at day: " + str(i) +" year: "+year)
            print(adress)
            continue
    plot_datapoints()
    plot_coordinates()
