import numpy as np
import time
from numba import njit
"""
the accuracy of a sample mean
"""

def filtering_outliers(z,verbose=False, t=np.array([False])):
    N = len(z)
    interval = 60
    ave_z = np.median(z)
    z_60 = abs(z-ave_z)
    z_temp = np.where(z_60 > 0.2,np.nan,z)
    z_temp = np.where(z_60 > 3*np.std(z),np.nan,z_temp)
    if verbose:
        print(100*(1-np.sum(np.isnan(z_temp))/N),"% filtered")
    if t.any():
        t =t[np.logical_not(np.isnan(z_temp))]
    z_resized = z_temp[np.logical_not(np.isnan(z_temp))]
    if t.any():
        return z,z_resized,t
    return z, z_resized


def accuracy_NMEA(z):
    """
    Calculates the noise over a time period t.
    """
    N = len(z); size = int(N-60)
    sigma = np.zeros(size)
    for i in range(30,N-30):
        z_ave = np.sum(z[(i-30):(i+30)])/60
        sigma[i-30] = ((np.sum( abs(z[i-30:i+30]-z_ave)**2 ) )/((60)-1))**0.5
    return sigma

@njit
def accuracy_NMEA_opt(z):
    """
    Calculates the noise over a time period t.
    """
    N = len(z); size = int(N-60)
    sigma = np.zeros(size)
    for i in range(30,N-30):
        z_ave = 0
        for z_ave_i in z[(i-30):(i+30)]:
            z_ave += z_ave_i
        z_ave = z_ave/60.

        noise_sqrt = 0
        for noise in z[i-30:i+30]:
            noise_sqrt += abs(noise - z_ave)**2
        sigma[i-30] = (noise_sqrt/(60.-1.))**0.5
    return sigma


if __name__ == '__main__':
    x = np.linspace(0,1,120000)
    y =np.sin(x)
    t1 = time.time()
    n =accuracy_NMEA(x)
    print(time.time()-t1)
    t2 = time.time()
    n_opt = accuracy_NMEA_opt(x)
    print(time.time()-t2)

    print(accuracy_NMEA(y), "y")
