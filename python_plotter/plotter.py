import numpy as np
import matplotlib.pyplot as plt
n = 10000
x = np.linspace(0,np.pi,n)
y = np.sin(x)
z = np.cos(x)
adress = "../../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
print(adress[52:55])

for i in range(100):
    if True:
        if i%10:
            continue
    print(i)

plt.subplot(2,1,1)
plt.title("")
plt.plot(x,y)
plt.ylabel("y")
plt.subplot(2,1,2)
plt.plot(x,z)
plt.ylabel("z")
plt.xlabel("x")
plt.savefig("../plots/noisy_data_small_1/test_picture.png")
