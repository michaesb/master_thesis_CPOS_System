import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

np.random.seed(1)

x = np.linspace(0,2*np.pi,100)
y = np.sin(x) + np.random.random(100) * 0.2
yhat = savgol_filter(y, 51, 3)
plt.plot(x,y)
plt.plot(x,yhat, "r-")
plt.show()
