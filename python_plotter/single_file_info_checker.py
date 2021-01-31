#!/usr/bin/env python3
import time, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, "..")
from data_reader_RTIM.RTIM_data_reader import ReadRTIMData

adress = sys.argv[1]
receiver_id = adress[52:55]

obj = ReadRTIMData()
obj.read_textfile_only_specication_info(adress)
obj.textdocument_version_display()
obj.receiver_display()
obj.display_date()
