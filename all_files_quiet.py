"""
Reading version 1.3
"""
import numpy as np
import matplotlib.pyplot as plt
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData
import time


adress_bod = "../../data_thesis/share_UiOMichael/Data/20200101/bod22020001.scn"
adress_far = "../../data_thesis/share_UiOMichael/Data/20200101/far22020001.scn"
adress_hof = "../../data_thesis/share_UiOMichael/Data/20200101/hof22020001.scn"
adress_hon = "../../data_thesis/share_UiOMichael/Data/20200101/hon22020001.scn"
adress_hop = "../../data_thesis/share_UiOMichael/Data/20200101/hop22020001.scn"
adress_jan = "../../data_thesis/share_UiOMichael/Data/20200101/jan22020001.scn"
adress_kau = "../../data_thesis/share_UiOMichael/Data/20200101/kau22020001.scn"
adress_nya = "../../data_thesis/share_UiOMichael/Data/20200101/nya22020001.scn"
adress_veg = "../../data_thesis/share_UiOMichael/Data/20200101/veg22020001.scn"


print("---------------------------")

bjn = ReadRTIMData()
bjn.read_textfile_only_specication_info(adress_bod)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()

print("---------------------------")

bod = ReadRTIMData()
bod.read_textfile_only_specication_info(adress_far)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

print("---------------------------")

bod = ReadRTIMData()
bod.read_textfile_only_specication_info(adress_hof)
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

bod = ReadRTIMData()
bod.read_textfile_only_specication_info(adress_jan)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

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
veg = ReadRTIMData()
veg.read_textfile_only_specication_info(adress_veg)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()


from termcolor import colored
print(colored('finneshed', 'green'))
