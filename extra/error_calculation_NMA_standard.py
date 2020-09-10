import numpy as np

"""
the accuracy of a sample mean
"""

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
