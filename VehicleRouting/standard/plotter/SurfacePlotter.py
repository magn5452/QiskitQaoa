import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


class SurfacePlotter:

    def __init__(self):
        pass

    def plot(self, fun):
        fig = plt.figure()

        ax = fig.add_subplot(projection='3d')

        ax.xaxis.pane.set_edgecolor('k')
        ax.yaxis.pane.set_edgecolor('k')
        ax.zaxis.pane.set_edgecolor('k')
        ax.xaxis.pane.set_alpha(1)
        ax.yaxis.pane.set_alpha(1)
        ax.zaxis.pane.set_alpha(1)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.invert_yaxis()
        ax.invert_xaxis()



        # Create the mesh X, Y and compute Z
        x_list = y_list = np.arange(0, np.pi/2, 0.2)
        X, Y = np.meshgrid(x_list, y_list)
        Z = np.zeros(X.shape)
        for ix, x in enumerate(x_list):
            for iy, y in enumerate(y_list):
                Z[ix, iy] = fun([x, y])
        ax.plot_surface(X, Y, Z, cmap=cm.rainbow, linewidth=0, antialiased=False, alpha=0.8)

        ax.set_xlabel(r'$\beta$')
        ax.set_ylabel(r'$\gamma$')
        ax.set_zlabel(r'$C(\theta)$')

        plt.show()
