import numpy as np
import time

def progress_bar(i,size,ending= "\r"):
    print("\033[95m", end= "\r")
    print(int(100*i/size), "%", end= ending)
    print("\033[39m", end ="\r")

if __name__ == '__main__':
    """
    simple test run of the progressbar
    """
    size = 200
    print ("press ctrl+z to exit from the progressbar")
    for i in range(size):
        progress_bar(i,size)
        time.sleep(0.2)
    for i in range(4):
        for j in range(100):
            print(i*100+j)
