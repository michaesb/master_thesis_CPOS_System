import numpy as np
import matplotlib.pyplot as plt
from data_reader_ROTI.ROTI_data_reader import ReadROTIData
import time,sys
# from extra import progressbar
adress_midnight = "../../data_thesis/data/RTIM/2015/03/17/ROTI/ROTI_20150317_0000to0059.txt"

frame = sys.argv[1]
mid = ReadROTIData()
mid.read_textfile(adress_midnight, True)
print("time",mid.time)
print("latitude,longitude", mid.coordinates)
data = mid.ROTI_Grid_data

#unfinished
