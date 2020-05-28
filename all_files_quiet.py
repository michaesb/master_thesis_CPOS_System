"""
Reading version 1.3
"""
import numpy as np
import matplotlib.pyplot as plt
from data_reader.data_reader_main import ReadData
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


print(1/9.)

bod = ReadData()
bod.read_textfile(adress_bod, False)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

print(2/9.)

bjn = ReadData()
bjn.read_textfile(adress_far, False)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()

print(3./9.)

hon = ReadData()
hon.read_textfile(adress_hof, False)
hon.textdocument_version_display()
hon.receiver_display()
hon.display_date()

print(4./9.)

hop = ReadData()
hop.read_textfile(adress_hon, False)
hop.textdocument_version_display()
hop.receiver_display()
hop.display_date()

print(5/9.)

kau = ReadData()
kau.read_textfile(adress_hop, False)
kau.textdocument_version_display()
kau.receiver_display()
kau.display_date()

print(6/9.)

nya = ReadData()
nya.read_textfile(adress_jan, False)
nya.textdocument_version_display()
nya.receiver_display()
nya.display_date()

print(7/9.)

tro = ReadData()
tro.read_textfile(adress_kau, False)
tro.textdocument_version_display()
tro.receiver_display()
tro.display_date()

print(8/9.)

veg = ReadData()
veg.read_textfile(adress_nya, False)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()

print(1)

veg = ReadData()
veg.read_textfile(adress_veg, False)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()


from termcolor import colored
print(colored('finneshed', 'green'))
