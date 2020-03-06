import numpy as np
import matplotlib.pyplot as plt
from data.data_reader import ReadData

obj = ReadData()
str ="data/example_data_ver_1_3.txt"
obj.read_textfile(str)


















from termcolor import colored
print( colored('hello', 'red'), colored('world', 'green'))
