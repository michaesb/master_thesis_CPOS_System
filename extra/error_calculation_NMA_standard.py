import numpy as np

"""
the accuracy of a sample mean
"""

def filtering_outliers(z,verbose=False):
    N = len(z)
    interval = 60
    z_copy = z.copy()
    for i in range(0,len(z),interval):
        ave_z = np.mean(z_copy[i:i+interval])
        z_60 = abs(z_copy[i:i+interval]-ave_z)
        z_temp = np.where(z_60 > 0.2,np.nan,z_copy[i:i+interval])
        z_temp = np.where(z_60 > 3*np.std(z_copy), np.nan,z_temp)
        z_copy[i:i+interval] = z_temp
    z_resized = z_copy[np.logical_not(np.isnan(z_copy))]
    if verbose:
        print(N,len(z_resized), "size of array", "percentage=", 100*len(z_resized)/N)
    return z, z_resized


def accuracy_NMEA(z):
    """
    Calculates the noise over a time period t.
    """
    N = len(z); size = int(N-60)
    sigma = np.zeros(size)
    for i in range(30,N-30):
        z_ave = np.sum(z[(i-30):(i+30)])/size
        sigma[i-30] = ((np.sum(abs(z[i-30:(i+30)]) - z_ave)**2 )/((60)-1))**0.5
    return sigma
