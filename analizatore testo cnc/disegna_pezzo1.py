import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_cnc_profile_2d(posizioni_percorso, posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti):
    fig, ax = plt.subplots()

    # Plot continuous lines for movement paths
    if posizioni_percorso:
        x, _, z = zip(*posizioni_percorso)
        ax.plot(x, z, label='Percorso', linewidth=0.5)

    # Plot final rapid movements
    if posizioni_finali_movimenti_rapidi:
        x, _, z = zip(*posizioni_finali_movimenti_rapidi)
        ax.plot(x, z, color='r', marker='o', linestyle='dashed', label='Movimenti Rapidi')

    # Plot final working movements
    if posizioni_finali_lavorazione:
        x, _, z = zip(*posizioni_finali_lavorazione)
        ax.plot(x, z, color='g', marker='^', linestyle='dashed', label='Lavorazione')

    ax.set_xlabel('X')
    ax.set_ylabel('Z')  # Cambiato da 'Y' a 'Z' per rispecchiare l'asse verticale
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    # Impostare gli assi in modo esplicito
    ax.set_aspect('equal', adjustable='box')
    
    # Calcolare il massimo tra gli estremi positivi e negativi per entrambi gli assi
    max_limit = max(max(ax.get_xlim()), max(ax.get_ylim()), abs(min(ax.get_xlim())), abs(min(ax.get_ylim())))
    
    # Impostare gli estremi degli assi in modo che lo zero corrisponda al centro
    ax.set_xlim(-max_limit, max_limit)
    ax.set_ylim(-max_limit, max_limit)

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
