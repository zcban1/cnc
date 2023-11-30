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
        ax.plot(z, x, color='g', linestyle='dashed', label='Lavorazione')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    ax.legend()
    plt.show()

def plot_cnc_profile_2d2(posizioni_finali_lavorazione, posizioni_finali_movimenti_rapidi,posizioni_percorso):
    fig, ax = plt.subplots()

    # Plot final working movements with a solid green line
    if posizioni_finali_lavorazione:
        x, _, z = zip(*posizioni_finali_lavorazione)
        for i, (xi, zi) in enumerate(zip(x, z), start=1):
            ax.plot(zi, xi, color='g', marker='^')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)

        # Connect points with a dashed line
        ax.plot(z, x, color='g', linestyle='dashed', label='Lavorazione')

    # Plot final rapid movements with a dashed red line
    if posizioni_finali_movimenti_rapidi:
        x_rapid, _, z_rapid = zip(*posizioni_finali_movimenti_rapidi)
        for i, (xi, zi) in enumerate(zip(x_rapid, z_rapid), start=1):
            ax.plot(zi, xi, color='r', marker='o', linestyle='dashed')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)

        ax.plot(z_rapid, x_rapid, color='r', marker='o', linestyle='dashed', label='Movimenti Rapidi')


    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    # Place legend outside the plot
    #ax.legend(bbox_to_anchor=(1., 1), loc='upper left')
    ax.legend(loc='upper left')

    plt.show()

def plot_cnc_profile_2d3(posizioni_percorso):
    fig, ax = plt.subplots()

    # Plot final working movements
    if posizioni_percorso:
        x, _, z = zip(*posizioni_percorso)
        
        # Plot points
        for i, (xi, zi) in enumerate(zip(x, z), start=1):
            ax.plot(zi, xi, color='violet', marker='^', linestyle='dashed')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)
        
        # Connect points with a dashed line
        ax.plot(z, x, color='g', linestyle='dashed', label='percorso')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    ax.legend()
    plt.show()

def plot_cnc_profile_2d4(posizioni_percorso, posizioni_finali_lavorazione,posizioni_finali_movimenti_rapidi):
    fig, ax = plt.subplots()

    # Plot final working movements
    if posizioni_percorso:
        x, _, z = zip(*posizioni_percorso)
        
        # Plot points for posizioni_percorso
        for i, (xi, zi) in enumerate(zip(x, z), start=1):
            ax.plot(zi, xi, color='violet', marker='^', linestyle='dashed')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)
        
        # Connect points for posizioni_percorso with a dashed green line
        ax.plot(z, x, color='g', linestyle='dashed', label='percorso')

    # Plot points and connect with a solid red line for posizioni_finali_lavorazione
    if posizioni_finali_lavorazione:
        x_final, _, z_final = zip(*posizioni_finali_lavorazione)
        ax.plot(z_final, x_final, color='red', linestyle='solid', marker='o', label='finali lavorazione')

     # Plot points as markers only for posizioni_finali_movimenti_rapidi
    if posizioni_finali_movimenti_rapidi:
        x_rapidi, _, z_rapidi = zip(*posizioni_finali_movimenti_rapidi)
        ax.scatter(z_rapidi, x_rapidi, color='purple', marker='s', label='finali movimenti rapidi')
    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    ax.legend()
    plt.show()


def plot_cnc_profile_2d5(posizioni_percorso, posizioni_finali_lavorazione, posizioni_finali_movimenti_rapidi):
    fig, ax = plt.subplots()

    # Plot final working movements
    if posizioni_percorso:
        x, _, z = zip(*posizioni_percorso)
        
        # Plot points for posizioni_percorso with markers
        for i, (xi, zi) in enumerate(zip(x, z), start=1):
            ax.plot(zi, xi, color='violet', marker='^', linestyle='dashed')
            ax.text(zi, xi, f'{i}', ha='right', va='bottom', fontsize=12)
        
        # Connect points for posizioni_percorso with a dashed green line
        ax.plot(z, x, color='g', linestyle='dashed', label='percorso')

    # Plot points as markers only for posizioni_finali_lavorazione
    if posizioni_finali_lavorazione:
        x_final, _, z_final = zip(*posizioni_finali_lavorazione)
        ax.scatter(z_final, x_final, color='red', marker='o', label='finali lavorazione')

    # Plot points as markers only for posizioni_finali_movimenti_rapidi
    if posizioni_finali_movimenti_rapidi:
        x_rapidi, _, z_rapidi = zip(*posizioni_finali_movimenti_rapidi)
        ax.scatter(z_rapidi, x_rapidi, color='purple', marker='s', label='finali movimenti rapidi')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_title('Profilo del Pezzo (Proiezione 2D)')

    plt.legend()
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


    ax.legend()
    plt.show()
