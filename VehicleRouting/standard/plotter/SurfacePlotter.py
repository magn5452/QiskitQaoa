import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from tqdm import tqdm
import time

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
        gamma_max = np.pi
        beta_max = np.pi
        gamma_list = np.arange(0, gamma_max, gamma_max / 20)
        beta_list = np.arange(0, beta_max, beta_max / 20)
        X, Y = np.meshgrid(beta_list, gamma_list)
        Z = np.zeros(X.shape)
        for i_gamma, gamma in tqdm(enumerate(gamma_list)):
            for i_beta, beta in enumerate(beta_list):
                Z[i_beta, i_gamma] = fun([beta, gamma])
        ax.plot_surface(X, Y, Z, cmap=cm.rainbow, linewidth=0, antialiased=False, alpha=0.8)

        ax.set_xlabel(r'$\gamma$')
        ax.set_ylabel(r'$\beta$')
        ax.set_zlabel(r'$C(\theta)$')

        plt.show()
