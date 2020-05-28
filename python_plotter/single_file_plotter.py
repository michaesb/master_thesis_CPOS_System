#!/usr/bin/env python3
import time, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader.data_reader_main import ReadData

print("command line arguments: ", sys.argv[:])
adress = sys.argv[1]



obj = ReadData()
obj.read_textfile(adress, True)
obj.textdocument_version_display()
obj.receiver_display()
obj.display_date()
L1_amplitude, L1_phase, L1_slope = obj.L1_data
L2_amplitude, L2_phase, L2_slope = obj.L2_data

print("L1_slope check of any non-zero ", np.sum(L1_slope!=0))
print("L2_slope check of any non-zero ", np.sum(L2_slope!=0))
x = np.linspace(0,24,len(L1_amplitude)) #temp
plt.subplot(2,1,1)
plt.plot(x,L1_amplitude)
plt.plot(x,L1_phase)
plt.legend(["Amplitude","Carrier"])
plt.title("L1 scintillation")
plt.ylabel("interference")



plt.subplot(2,1,2)
plt.plot(x,L2_amplitude)
plt.plot(x,L2_phase)
plt.legend(["Amplitude","Carrier"])
plt.xlabel("time [min]")
plt.ylabel("interference")
plt.show()
