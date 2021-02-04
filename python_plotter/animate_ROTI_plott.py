#!/usr/bin/env python3
import time, sys, os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_ROTI.ROTI_data_reader import ReadROTIData
from scipy.ndimage.interpolation import rotate
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.animation import FuncAnimation

# adress "../../../../../run/media/michaelsb/data_ssd/data/RTIM/2018/01/01/ROTI/"


fig, ax = plt.subplots()
def plot_the_grid(i):
    ax.imshow(data[:,60:,i],cmap="magma")
    ax.set_title("date: "+date[0:4]+" "+date[4:6]+" "+date[6:8]+\
    " time"+str(i[-14:-12])+":"+str(int(time_of_grid[ii])))
    ax.set_xlabel("longitude")
    ax.set_xticks(np.linspace(0,50,nr_xticks), minor = False)
    ax.set_xticklabels(x_labels.tolist())
    ax.set_ylabel("latitude")
    ax.set_yticks(np.linspace(0,30,nr_yticks), minor = False)
    ax.set_yticklabels(y_labels.tolist())
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    sm = plt.cm.ScalarMappable(cmap="magma", norm=plt.Normalize(vmin=0, vmax=5))
    fig.colorbar(sm, cax=cax)


try:
    month, date = sys.argv[1][0:2], sys.argv[1][2:]
    print("month",month,"date",date)
    adress_folder = "/run/media/michaelsb/data_ssd/data/RTIM/2018/"+month+"/"+date+"/ROTI/"
except IndexError:
    adress_folder = "/run/media/michaelsb/data_ssd/data/RTIM/2018/06/02/ROTI/"

date = adress_folder[40:44] +adress_folder[45:47]+adress_folder[48:50]
date_plotting_path = adress_folder[40:44] +"/"+adress_folder[45:47]+"/"+adress_folder[48:50]
date_folder = "ROTI_" +date_plotting_path+"/"
folder_path = "../plots/"+date_folder

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

adresses = []

for i in range(24):
    if len(str(i))==1:
        adress_temp = adress_folder + "ROTI_"+ date +"_0"+str(i)+"00to0"+str(i)+"59.txt"
        adresses.append(adress_temp)
    else:
        adress_temp = adress_folder + "ROTI_"+ date +"_"+str(i)+"00to"+str(i)+"59.txt"
        adresses.append(adress_temp)
time1 = time.time()

for i in adresses:
    ROTI_data = ReadROTIData()
    try:
        ROTI_data.read_textfile(i, False)
    except FileNotFoundError:
        continue
    print("longitude, latitude", ROTI_data.coordinates)
    path = folder_path + "/"
    data = ROTI_data.ROTI_Grid_data
    time_of_grid = ROTI_data.time
    x_axis,y_axis = ROTI_data.coordinates[0],ROTI_data.coordinates[1]


    x_labels = np.arange(-10,x_axis[1]+10,10,dtype=int)
    y_labels = np.arange(y_axis[1],y_axis[0]+5,-5,dtype=int)
    nr_yticks = len(y_labels)
    nr_xticks = len(x_labels)

    animate = FuncAnimation(fig,plot_the_grid)
    plt.show()
