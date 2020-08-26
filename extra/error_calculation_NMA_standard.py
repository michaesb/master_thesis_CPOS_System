import numpy as np



def accuracy_NMEA(x):
  """
  Calculates the noise over a time period t.
  Assumes that the length of the vector is 60
  """
  length= 60
  if not len(z)==length:
     raise ValueError("the length of input variable is not 60")
  sigma = 1./(N-1)
  
  sigma = sigma*np.sum( abs(x - np.sum(x)/length)**2 )
  
  sigma = sigma**0.5 #root of sigma

  return sigma
