import numpy as np
import matplotlib.pyplot as plt
n = 10000
x = np.linspace(0,np.pi,n)
y = np.sin(x)
z = np.cos(x)
adress = "../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
plt.subplot(2,1,1)
plt.title("")
plt.plot(x,y)
plt.ylabel("y")
plt.subplot(2,1,2)
plt.plot(x,z)
plt.ylabel("z")
plt.xlabel("x")
plt.show()
