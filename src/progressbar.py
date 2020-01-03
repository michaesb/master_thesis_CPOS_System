import numpy as np
import time

def progress_bar(i,size):
    print(int(100*i/size), "%", end= "\r")

if __name__ == '__main__':
    """
    simple test run of the progressbar
    """
    size = 200
    print ("press ctrl+z to exit from the progressbar")
    for i in range(size):
        progress_bar(i,size)
        time.sleep(0.2)
