import numpy as np

"""
the accuracy of a sample mean
"""


def filtering_outliers(z):
    N = len(z)
    interval = 60
    z_copy = z.copy()
    for i in range(0,len(z),interval):
        ave_z = np.mean(z_copy[i:i+interval])
        z_60 = abs(z_copy[i:i+interval]-ave_z)
        z_temp = np.where( z_60 > 0.2,np.nan,z_copy[i:i+interval])
        z_temp = np.where( z_60 > 3*np.std(z_copy), np.nan,z_temp)
        z_copy[i:i+interval] = z_temp
    z_resized = z_copy[np.logical_not(np.isnan(z_copy))]

    print(N,len(z_resized), "size of array", "percentage=", 100*len(z_resized)/N)
    return z, z_resized


def accuracy_NMEA(z):
    """
    Calculates the noise over a time period t.
    """
    N = len(z); size = int(np.floor(N)/60)
    sigma = np.zeros(size+1)
    for i in range(0,N,60):
        z_ave = np.sum(z[i:(i+60)])/size
        sigma[int(i/60)] = ((np.sum(abs(z[i:(i+60)]) - z_ave)**2 )/((60)-1))**0.5
    return sigma
