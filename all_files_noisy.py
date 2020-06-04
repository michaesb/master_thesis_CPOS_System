"""
Reading version 1.1
"""
import numpy as np
import matplotlib.pyplot as plt
from data_reader.RTIM_data_reader import ReadRTIMData
import time
adress_bjo = "../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
adress_bod = "../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn"
adress_hon = "../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn"
adress_hop = "../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn"
adress_kau = "../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn"
adress_nya = "../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn"
adress_tro = "../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn"
adress_veg = "../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn"

print(1/8.)

bjn = ReadRTIMData()
bjn.read_textfile(adress_bjo, True)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()

print(2/8.)

bod = ReadRTIMData()
bod.read_textfile(adress_bod, True)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

print(3./8.)

hon = ReadRTIMData()
hon.read_textfile(adress_hon, True)
hon.textdocument_version_display()
hon.receiver_display()
hon.display_date()

print(4./8)

hop = ReadRTIMData()
hop.read_textfile(adress_hop, True)
hop.textdocument_version_display()
hop.receiver_display()
hop.display_date()

print(5/8.)

kau = ReadRTIMData()
kau.read_textfile(adress_kau, True)
kau.textdocument_version_display()
kau.receiver_display()
kau.display_date()

print(6/8.)

nya = ReadRTIMData()
nya.read_textfile(adress_nya, True)
nya.textdocument_version_display()
nya.receiver_display()
nya.display_date()

print(7/8.)

tro = ReadRTIMData()
tro.read_textfile(adress_tro, True)
tro.textdocument_version_display()
tro.receiver_display()
tro.display_date()

print(1)
veg = ReadRTIMData()
veg.read_textfile(adress_veg, True)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()


from termcolor import colored
print(colored('finneshed', 'green'))
