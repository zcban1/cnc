import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

comandi_cnc = {
    "G00": "Movimento rapido",
    "G0": "Movimento rapido",
    "G01": "Movimento lineare",
    "G1": "Movimento lineare",
    "G02": "Interpolazione circolare oraria",
    "G2": "Interpolazione circolare oraria",    
    "G03": "Interpolazione circolare antioraria",
    "G3": "Interpolazione circolare antioraria",
    "G04": "Pausa programma",
    "G4": "Pausa programma",
    "G96": "Velocità costante del mandrino",
    "G97": "Velocità costante del mandrino con RPM",
    "M03": "Accendi mandrino in senso orario",
    "M04": "Accendi mandrino in senso antiorario",
    "M05": "Spegni mandrino",
    "M28": "apertura serrapinza",
    "M29": "chiusura serrapinza",
    "T01": "Cambia utensile a posizione 1",
    "T02": "Cambia utensile a posizione 2",
    "S": "Imposta la velocità del mandrino",
    "I": "Coordinate X del centro della circonferenza",
    "J": "Coordinate Y del centro della circonferenza",
    "X": "Coordinate X",
    "Y": "Coordinate Y",
    "Z": "Coordinate Z",
}

def converti_velocita_in_rpm(velocita):
    try:
        return int(velocita)
    except ValueError:
        return "N/D"

def calcola_centro(posizione_attuale, i, j):
    centro_x = posizione_attuale['X'] + float(i)
    centro_y = posizione_attuale['Y'] + float(j)
    return centro_x, centro_y

def analizza_file_cnc(nome_file):
    posizioni_x = []
    posizioni_y = []
    posizioni_z = []
    commenti = []
    
    try:
        with open(nome_file, 'r') as file_cnc:
            righe = file_cnc.readlines()
            posizione_attuale = {'X': 0, 'Y': 0, 'Z': 0}

            for numero_riga, riga in enumerate(righe, start=1):
                comando, *parametri = riga.strip().split()  # Assume che il comando sia la prima parola nella riga
                significato = comandi_cnc.get(comando, "Comando sconosciuto")

                if comando == "S" and parametri:
                    velocita = parametri[0]
                    significato += f" - Velocità: {velocita} RPM"
                elif comando in ["G96"] and parametri:
                    velocita = converti_velocita_in_rpm(parametri[0].lstrip("S"))
                    significato += f" - Velocità del mandrino: {velocita} RPM"
                elif comando in ["G02", "G03","G2", "G3"] and len(parametri) >= 3:
                    i = parametri[-2].lstrip("I")
                    j = parametri[-1].lstrip("J")
                    centro_x, centro_y = calcola_centro(posizione_attuale, i, j)
                    significato += f" - Centro: (I={i}, J={j}) - Posizione del centro: (X={centro_x}, Y={centro_y})"
                elif comando in ["G00", "G01", "G02", "G03","G0", "G1", "G2", "G3"] and parametri:
                    param_dict = {p[0]: p[1:] for p in parametri}
                    posizione_attuale.update({k: float(v) for k, v in param_dict.items()})
                    
                    x = posizione_attuale.get("X", "N/D")
                    y = posizione_attuale.get("Y", "N/D")
                    z = posizione_attuale.get("Z", "N/D")
                    significato += f" - Posizione: (X={x}, Y={y}, Z={z})"
                    posizioni_x.append(posizione_attuale.get("X", 0))
                    posizioni_y.append(posizione_attuale.get("Y", 0))
                    posizioni_z.append(posizione_attuale.get("Z", 0))
              

                print(f'Riga {numero_riga}: {riga.strip()} - {significato}')

                # Gestione dei commenti all'interno delle parentesi tonde
                commento = None
                if '(' in riga and ')' in riga:
                    commento = riga[riga.find('(') + 1:riga.find(')')]
                    commenti.append(f'Riga {numero_riga}: {commento}')

    except FileNotFoundError:
        print(f"Errore: Il file {nome_file} non esiste.")
    except Exception as e:
        print(f"Errore durante l'apertura del file: {e}")

    return posizioni_x, posizioni_y,posizioni_y,commenti

def disegna_tornio_percorso(posizioni_x, posizioni_y, posizioni_z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(posizioni_z, posizioni_x, posizioni_y, marker='o', linestyle='-')  # Specify linestyle
    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')
    plt.title('Percorso Tornio CNC')
    plt.show()

if __name__ == "__main__":
    nome_file_cnc = "CNC_modificato.txt"
    posizioni_x,posizioni_z, posizioni_y, commenti = analizza_file_cnc(nome_file_cnc)
    # Stampa i commenti nello stesso numero di righe del file
    print("\nCommenti:")
    for commento in commenti:
        print(commento)
    disegna_tornio_percorso(posizioni_x, posizioni_y,posizioni_z)


