import numpy as np
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
    print(np.sum(np.isnan(z_temp)))
    if t.any():
        t = np.where(np.isnan(z_temp),np.nan,t)
        t =t[np.logical_not(np.isnan(t))]
        print(len(t),"t", len(z))
        z_resized = z_temp[np.logical_not(np.isnan(z_temp))]
        return z,z_resized,t
    z_resized = z_temp[np.logical_not(np.isnan(z_temp))]
    return z, z_resized


def accuracy_NMEA(z):
    """
    Calculates the noise over a time period t.
    """
    N = len(z); size = int(N-60)
    sigma = np.zeros(size)
    for i in range(30,N-30):
        z_ave = np.sum(z[(i-30):(i+30)])/60
        sigma[i-30] = (((np.sum( abs(z[i-30:(i+30)]-z_ave) )**2 )/((60)-1)))**0.5
    return sigma
