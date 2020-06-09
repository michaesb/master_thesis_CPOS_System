import numpy as np
import matplotlib.pyplot as plt
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData
import time
# from extra import progressbar
adress_bjn = "../../data_thesis/kartverket/data/RTIM/2015/bjo22015076.scn"


bjn = ReadRTIMData()
bjn.read_textfile(adress_bjn, True, True)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()
L1_amplitude, L1_phase = bjn.L1_data
L2_amplitude, L2_phase = bjn.L2_data
t = bjn.time(unit=1) #hours


plt.plot(t,L1_amplitude)
plt.plot(t,L1_phase)
plt.legend(["Amplitude","Carrier"])
plt.title("L1 scintillation")
plt.ylabel("interference")
plt.show()


plt.plot(t,L2_amplitude)
plt.plot(t,L2_phase)
plt.legend(["Amplitude","Carrier"])
plt.xlabel("time[minutes] ")
plt.ylabel("interference")
plt.show()
