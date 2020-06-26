#!/usr/bin/env python3
import time, sys, os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_ROTI.ROTI_data_reader import ReadROTIData
from scipy.ndimage.interpolation import rotate




adress_folder = "../../../data_thesis/data/RTIM/2015/06/23/ROTI/"

date = adress_folder[31:35] +adress_folder[36:38]+adress_folder[39:41]
date_plotting_path = adress_folder[31:35] +"/"+adress_folder[36:38]+"/"+adress_folder[39:41]
date_folder = "ROTI_" +date_plotting_path+"/"
folder_path = "../plots/"+date_folder
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


adresses = []

for i in range(24):
    if len(str(i))==1:
        adress_temp = adress_folder + "ROTI_"+str(date)+ "_0"+str(i)+"00to0"+str(i)+"59.txt"
        adresses.append(adress_temp)
    else:
        adress_temp = adress_folder + "ROTI_"+str(date)+ "_"+str(i)+"00to"+str(i)+"59.txt"
        adresses.append(adress_temp)

for i in adresses:
    print(i) #../../../data_thesis/data/RTIM/2015/06/22/ROTI/ROTI_20150622_0000to0059.txt

    ROTI_data = ReadROTIData()
    ROTI_data.read_textfile(i, True)
    print("time",ROTI_data.time)
    print("latitude,longitude", ROTI_data.coordinates)
    path = folder_path + "/"

    data = np.sum(ROTI_data.ROTI_Grid_data,axis=2)
    plt.imshow(data)
    # plt.show()
    plt.savefig(folder_path+str(i[61:71]))
