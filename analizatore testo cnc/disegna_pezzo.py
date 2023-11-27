import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_cnc_profile_2d(posizioni_finali_lavorazione):
    fig, ax = plt.subplots()

    # Plot final working movements
    if posizioni_finali_lavorazione:
        x, _, z = zip(*posizioni_finali_lavorazione)
        
        # Plot points
        for i, (xi, zi) in enumerate(zip(x, z), start=1):
            ax.plot(zi, xi, color='g', marker='^', linestyle='dashed')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)
        
        # Connect points with a dashed line
        ax.plot(z, x, color='g', linestyle='dashed', label='Linea Tratteggiata')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    ax.legend()
    plt.show()




def plot_cnc_profile(posizioni_finali_lavorazione):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    # Plot final working movements
    if posizioni_finali_lavorazione:
        x, y, z = zip(*posizioni_finali_lavorazione)
        ax.plot(z, x, y, color='g', marker='^', linestyle='dashed', label='Lavorazione')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')
    ax.set_title('Profilo del Pezzo')

    ax.legend()
    plt.show()
