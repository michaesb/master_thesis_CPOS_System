import numpy as np
import matplotlib.pyplot as plt


def date_to_days(dates,year=2018):
    """
    a date in 2018 in to the number of day in the year by using the numpy
    package datetime64
    """
    doy = np.zeros(len(dates))
    for i in range(len(dates)):
        doy[i] = (dates[i] - np.datetime64(str(year)+"-01-01"))\
             /np.timedelta64(1,"D") + 1
    return doy
