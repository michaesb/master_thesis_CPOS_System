#!/usr/bin/env python3
import time, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData


adress = sys.argv[1]

receiver_id = adress[52:55]

obj = ReadRTIMData()
obj.read_textfile(adress, True,True)
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
          " at 17 january")
plt.ylabel("L1 scintillations")

plt.subplot(2,1,2)
plt.plot(t,L2_amplitude)
plt.plot(t,L2_phase)
plt.legend(["Amplitude","Carrier"])
plt.xlabel("time [min]")
plt.ylabel("L2 scintillations")
plt.show()
#plt.savefig("../plots/noisy_data_small_1_filtered/noisy_plot_24_hour_"+receiver_id)
