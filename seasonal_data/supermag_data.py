import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent

obj = ReadSubstormEvent()


try:
    path = "/scratch/michaesb/substorm_event_list_2018.csv"
    obj.read_csv(path)

except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/substorm_event_list_2018.csv"
    obj.read_csv(path)
    
def filtering_to_Norway_night(X):
    X_filtered = X
    return X_filtered
