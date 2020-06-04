import numpy as np
import matplotlib.pyplot as plt
from data_reader.RTIM_data_reader import ReadRTIMData
import time
# from extra import progressbar
adress_bjn = "../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"


bjn = ReadRTIMData()
bjn.read_textfile(adress_bjn, True, True)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()
L1_amplitude, L1_phase, L1_slope = bjn.L1_data
L2_amplitude, L2_phase, L2_slope = bjn.L2_data
t = bjn.time(unit=1) #minutes
print()
print("L1_slope check of any non-zero ",np.sum(L1_slope!=0))
print("L2_slope check of any non-zero ",np.sum(L2_slope!=0))


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
