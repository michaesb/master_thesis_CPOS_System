#!/usr/bin/env python3
import time, sys, os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData
#/home/michaelsb/data_thesis/data/RTIM/2015/03/18/Scintillation


adress_midnight = "../../data_thesis/data/RTIM/2015/03/17/ROTI/ROTI_20150317_0000to0059.txt"

frame = sys.argv[1]
mid = ReadROTIData()
mid.read_textfile(adress_midnight, True)
print("time",mid.time)
print("latitude,longitude", mid.coordinates)
data = mid.ROTI_Grid_data

plt.imshow(data[:,:,frame])
plt.colorbar()
plt.show()

frame = sys.argv[1]

adress = sys.argv[2]

receiver_id = adress[56:59]

date = adress[31:41]
folder_path = "../plots/"+date
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
path = folder_path + "/plot_24_hour_"+receiver_id

def plotting(receiver_id,type):
    obj = ReadRTIMData()
    obj.read_textfile(adress,True,True)
    obj.textdocument_version_display()
    obj.receiver_display()
    obj.display_date()
    L1_amplitude, L1_phase = obj.L1_data
    L2_amplitude, L2_phase = obj.L2_data
    t = obj.time(unit=1) #retriving the hours from the data

    plt.subplot(2,1,1)
    plt.plot(t,L1_amplitude)
    plt.plot(t,L1_phase)
    plt.legend(["Amplitude","Carrier"])
    plt.title("L1 and L2 scintillation with receiver: "+receiver_id+\
              " at: " +date)
    plt.ylabel("L1 scintillations")

    plt.subplot(2,1,2)
    plt.plot(t,L2_amplitude)
    plt.plot(t,L2_phase)
    plt.legend(["Amplitude","Carrier"])
    plt.xlabel("time [hours]")
    plt.ylabel("L2 scintillations")
    plt.savefig(path)
    plt.show()
