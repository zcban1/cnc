import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

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
    posizioni_percorso = []
    posizioni_finali_movimenti_rapidi = []
    posizioni_finali_lavorazione = []
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
                elif comando in ["G04", "G4"] and parametri:
                    # Extract the numerical value after the X character
                    pause_duration_match = re.search(r'X(-?\d+(\.\d+)?)', ' '.join(parametri))
                    if pause_duration_match:
                        pause_duration = float(pause_duration_match.group(1))
                        significato += f" - Pausa di {pause_duration} secondi"
                
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
                    posizioni_percorso.append((posizione_attuale.get("X", 0), posizione_attuale.get("Y", 0), posizione_attuale.get("Z", 0)))

                    if comando in ["G00", "G0"]:
                        posizioni_finali_movimenti_rapidi.append((x, y, z))
                    else:
                        posizioni_finali_lavorazione.append((x, y, z))

                print(f'Riga {numero_riga}: {riga.strip()} - {significato}')
                #print("Posizioni movimenti rapidi:", posizioni_finali_movimenti_rapidi)

                # Gestione dei commenti all'interno delle parentesi tonde
                commento = None
                if '(' in riga and ')' in riga:
                    commento = riga[riga.find('(') + 1:riga.find(')')]
                    commenti.append(f'Riga {numero_riga}: {commento}')

    except FileNotFoundError:
        print(f"Errore: Il file {nome_file} non esiste.")
    except Exception as e:
        print(f"Errore durante l'apertura del file: {e}")

    return posizioni_percorso , posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti

def disegna_tornio_percorso(posizioni_percorso):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(*zip(*posizioni_percorso), marker='o', linestyle='-')  # Specify linestyle
    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')
    plt.title('Percorso Tornio CNC')
    plt.show()
    
#def disegna_tornio_pezzo(posizioni_finali):
    #fig, ax = plt.subplots()
    #ax.scatter(*zip(*posizioni_finali), marker='o')
    #ax.set_xlabel('X')
    #ax.set_ylabel('Y')
    #plt.title('Disegno Approssimato del Pezzo Finito')
    #plt.show()

def disegna_tornio_pezzo(posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione):
    fig, ax = plt.subplots()

    # Estrai le coordinate x, y, z dai dati per i movimenti rapidi
    x_rapidi, _, z_rapidi = zip(*posizioni_finali_movimenti_rapidi)
    
    # Estrai le coordinate x, y, z dai dati per le fasi di lavorazione
    x_lavorazione, _, z_lavorazione = zip(*posizioni_finali_lavorazione)

    # Unisci i punti dei movimenti rapidi con una linea tratteggiata e colore giallo
    ax.plot(z_rapidi, x_rapidi, marker='o', linestyle='--', color='yellow', label='Movimenti Rapidi')

    # Unisci i punti delle fasi di lavorazione con una linea continua e colore rosso
    ax.plot(z_lavorazione, x_lavorazione, marker='o', linestyle='-', color='red', label='Lavorazione')

    # Aggiungi etichette numeriche ai punti in base all'ordine in posizioni_finali
    for i, (x, _, z) in enumerate(posizioni_finali_movimenti_rapidi, start=1):
        ax.text(z, x, str(i), color='black', fontsize=8, ha='center', va='center')

    for i, (x, _, z) in enumerate(posizioni_finali_lavorazione, start=1):
        ax.text(z, x, str(i), color='black', fontsize=8, ha='center', va='center')

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    plt.title('Disegno Approssimato del Pezzo Finito')
    plt.legend()
    plt.show()





if __name__ == "__main__":
    nome_file_cnc = "CNC_modificato.txt"
    posizioni_percorso,  posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti  = analizza_file_cnc(nome_file_cnc)
    # Stampa i commenti nello stesso numero di righe del file
    print("\nCommenti:")
    for commento in commenti:
        print(commento)
    #disegna_tornio_percorso(posizioni_percorso)
    disegna_tornio_pezzo(posizioni_finali_movimenti_rapidi,posizioni_finali_lavorazione)
