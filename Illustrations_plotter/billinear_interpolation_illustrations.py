import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def bilinear_interpolation_plot():
    fig = plt.figure(figsize=(7,6))
    n = 1000
    z1 = np.linspace(0,0.8,n)
    z2 = np.linspace(0,1.5,n)
    z3 = np.linspace(0,1.9,n)
    z4 = np.linspace(0,3,n)

    ax = fig.add_subplot(111, projection='3d')
    points= [[1,1],[1,2],[2,1],[2,2]]
    intersection_point = [1.7,1.35]
    # points from the bottom
    ax.plot(points[0][0]*np.ones(n),points[0][1]*np.ones(n),z1,linewidth = 3,color="blue",alpha=0.4)
    ax.plot(points[1][0]*np.ones(n),points[1][1]*np.ones(n),z2,linewidth = 3,color="blue",alpha=0.4)
    ax.plot(points[2][0]*np.ones(n),points[2][1]*np.ones(n),z3,linewidth = 3,color="blue",alpha=0.4)
    ax.plot(points[3][0]*np.ones(n),points[3][1]*np.ones(n),z4,linewidth = 3,color="blue",alpha=0.4)
    ax.scatter(points[0][0],points[0][1],z1[-1],linewidth = 3,color="blue",alpha=0.6)
    ax.scatter(points[1][0],points[1][1],z2[-1],linewidth = 3,color="blue",alpha=0.6)
    ax.scatter(points[2][0],points[2][1],z3[-1],linewidth = 3,color="blue",alpha=0.6)
    ax.scatter(points[3][0],points[3][1],z4[-1],linewidth = 3,color="blue",alpha=0.6)

    #lines between points
    x_13 =np.linspace(points[0][0],points[3][0],n)
    zz13 = np.linspace(z1[-1],z3[-1],n)
    zz24 = np.linspace(z2[-1],z4[-1],n)
    ax.plot(x_13,np.ones(n)*1,zz13,linewidth = 2.0,color="red",alpha= 0.5)
    ax.plot(x_13,np.ones(n)*2,zz24,linewidth = 2.0,color="red",alpha= 0.5)
    # line between line
    y_13 = x_13
    index_z_x =int((intersection_point[0]-1)*1000)-1
    z_line = np.linspace(zz13[index_z_x],zz24[index_z_x],n)
    ax.plot(intersection_point[0]*np.ones(n),y_13,z_line,linewidth=2.5,color="purple")
    ax.scatter(intersection_point[0],y_13[0],z_line[0],linewidth=2.5,color="purple")
    ax.scatter(intersection_point[0],y_13[-1],z_line[-1],linewidth=2.5,color="purple")
    # point at the line
    z_point_5 = z_line[int((intersection_point[1]-1)*1000)-1]
    z5 = np.linspace(0,z_point_5,n)
    ax.plot(intersection_point[0]*np.ones(n),intersection_point[1]*np.ones(n),z5,linewidth = 3.5,color = "green",alpha=0.6)
    ax.scatter(intersection_point[0],intersection_point[1],z_point_5, color="green",linewidth=6)

    plt.tight_layout()
    plt.style.use("../format_for_latex.mplstyle")
    ax.set_xlabel('x')
    ax.set_xticks([1,2])
    ax.set_ylabel('y')
    ax.set_yticks([1,2])
    ax.set_zlabel('z')
    ax.set_zticks([])
    plt.tight_layout()
    plt.show()



bilinear_interpolation_plot()
