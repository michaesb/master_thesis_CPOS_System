import numpy as np
import matplotlib.pyplot as plt
from data_reader.data_reader_main import ReadData
import time
adress_bjn = "../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
adress_bod = "../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn"
adress_hon = "../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn"
adress_hop = "../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn"
adress_kau = "../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn"
adress_nya = "../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn"
adress_tro = "../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn"
adress_veg = "../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn"

print(1/8.)

bjn = ReadData()
bjn.read_textfile(adress_bjn, True)
bjn.textdocument_version_display()
bjn.receiver_display()
bjn.display_date()

print(2/8.)

bod = ReadData()
bod.read_textfile(adress_bod, True)
bod.textdocument_version_display()
bod.receiver_display()
bod.display_date()

print(3./8.)

hon = ReadData()
hon.read_textfile(adress_hon, True)
hon.textdocument_version_display()
hon.receiver_display()
hon.display_date()

print(4./8)

hop = ReadData()
hop.read_textfile(adress_hop, True)
hop.textdocument_version_display()
hop.receiver_display()
hop.display_date()

print(5/8.)

kau = ReadData()
kau.read_textfile(adress_kau, True)
kau.textdocument_version_display()
kau.receiver_display()
kau.display_date()

print(6/8.)

nya = ReadData()
nya.read_textfile(adress_nya, True)
nya.textdocument_version_display()
nya.receiver_display()
nya.display_date()

print(7/8.)

tro = ReadData()
tro.read_textfile(adress_tro, True)
tro.textdocument_version_display()
tro.receiver_display()
tro.display_date()

print(1)
veg = ReadData()
veg.read_textfile(adress_veg, True)
veg.textdocument_version_display()
veg.receiver_display()
veg.display_date()


from termcolor import colored
print(colored('finneshed', 'green'))
