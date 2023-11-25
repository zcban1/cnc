import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_cnc_profile_2d(posizioni_percorso, posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti):
    fig, ax = plt.subplots()

    # Plot continuous lines for movement paths
    if posizioni_percorso:
        x, y, _ = zip(*posizioni_percorso)
        ax.plot(x, y, label='Percorso', linewidth=0.5)

    # Plot final rapid movements
    if posizioni_finali_movimenti_rapidi:
        x, y, _ = zip(*posizioni_finali_movimenti_rapidi)
        ax.plot(x, y, color='r', marker='o', linestyle='dashed', label='Movimenti Rapidi')

    # Plot final working movements
    if posizioni_finali_lavorazione:
        x, y, _ = zip(*posizioni_finali_lavorazione)
        ax.plot(x, y, color='g', marker='^', linestyle='dashed', label='Lavorazione')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    ax.legend()
    plt.show()


def plot_cnc_profile(posizioni_percorso, posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot continuous lines for movement paths
    if posizioni_percorso:
        x, y, z = zip(*posizioni_percorso)
        ax.plot(x, y, z, label='Percorso', linewidth=0.5)

    # Plot final rapid movements
    if posizioni_finali_movimenti_rapidi:
        x, y, z = zip(*posizioni_finali_movimenti_rapidi)
        ax.plot(x, y, z, color='r', marker='o', linestyle='dashed', label='Movimenti Rapidi')

    # Plot final working movements
    if posizioni_finali_lavorazione:
        x, y, z = zip(*posizioni_finali_lavorazione)
        ax.plot(x, y, z, color='g', marker='^', linestyle='dashed', label='Lavorazione')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Profilo del Pezzo')

    ax.legend()
    plt.show()
