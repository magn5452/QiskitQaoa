import numpy as np
from matplotlib import pyplot as plt


class SurfacePlotter:

    def __init__(self):
        pass

    def plot(self, fun):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x_list = y_list = np.arange(0, np.pi/2, 0.1)
        X, Y = np.meshgrid(x_list, y_list)
        Z = np.zeros(X.shape)
        for ix, x in enumerate(x_list):
            for iy, y in enumerate(y_list):
                Z[ix, iy] = fun([x, y])
        ax.plot_surface(X, Y, Z)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
