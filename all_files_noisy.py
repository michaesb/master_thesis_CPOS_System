"""
Reading version 1.1
"""
import numpy as np
import matplotlib.pyplot as plt
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData
import time
adress_bjo = "../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
adress_bod = "../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn"
adress_hon = "../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn"
adress_hop = "../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn"
adress_kau = "../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn"
adress_nya = "../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn"
adress_tro = "../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn"
adress_veg = "../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn"

print("---------------------------")

bjn = ReadRTIMData()
bjn.read_textfile_only_specication_info(adress_bjo)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()

print("---------------------------")

bod = ReadRTIMData()
bod.read_textfile_only_specication_info(adress_bod)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

print("---------------------------")

hon = ReadRTIMData()
hon.read_textfile_only_specication_info(adress_hon)
hon.textdocument_version_display()
hon.receiver_display()
hon.display_date()

print("---------------------------")

hop = ReadRTIMData()
hop.read_textfile_only_specication_info(adress_hop)
hop.textdocument_version_display()
hop.receiver_display()
hop.display_date()

print("---------------------------")

kau = ReadRTIMData()
kau.read_textfile_only_specication_info(adress_kau)
kau.textdocument_version_display()
kau.receiver_display()
kau.display_date()

print("---------------------------")

nya = ReadRTIMData()
nya.read_textfile_only_specication_info(adress_nya,)
nya.textdocument_version_display()
nya.receiver_display()
nya.display_date()

print("---------------------------")

tro = ReadRTIMData()
tro.read_textfile_only_specication_info(adress_tro)
tro.textdocument_version_display()
tro.receiver_display()
tro.display_date()

print("---------------------------")
veg = ReadRTIMData()
veg.read_textfile_only_specication_info(adress_veg)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()


from termcolor import colored
print(colored('finneshed', 'green'))
