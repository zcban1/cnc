import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

precedente_comando_g = None  # Inizializza la variabile per il comando G precedente
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
    "G98": "avanzamento barra caricatore millimetri/minuto",
    "G99": "necessario per annullare G98 per tornare a lavorare in millimetri/giro",
    "M03": "Accendi mandrino in senso orario",
    "M04": "Accendi mandrino in senso antiorario",
    "M05": "Spegni mandrino",
    "M28": "Apertura Serrapinza/Autocentrante",
    "M29": "Chiusura Serrapinza/Autocentrante",
    "T101": "Cambia utensile 1 con correttore 01",
    "T800": "Cambia utensile 8 con correttore 00(correttore 00 non esiste annullera tutte le correzioni sulla T selezionata)",
    "T202": "Cambia utensile 2 con correttore 02",

    "S": "Imposta la velocità del mandrino",
    "F": "Imposta la velocità avanzamento torretta in lavorazione",
    "I": "Coordinate X del centro della circonferenza",
    "J": "Coordinate Y del centro della circonferenza",
    "X": "Coordinate X",
    "Y": "Coordinate Y",
    "Z": "Coordinate Z",
    "A": "Calcola Angolo",
    "M98": "Chiamata di sotto-programma",
    "M99": "Fine del sotto-programma",
    "M07": "Accendi acqua uscita dall'utensile",
    "M08": "Accendi acqua ",
    "M09": "Spegni acqua",
    "M40": "alza il braccetto prendi pezzo",
    "M41": "abbassa il braccetto prendi pezzo",
    "M43": "apertura portellone ",
    "N": "Numero Blocco Programma",
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

                # Handle tool change commands (e.g., N16 T116)
                if riga.startswith("N") and "T" in riga:
                    # Extract the tool change command components
                    n_index = riga.find("N") + 1
                    t_index = riga.find("T")
                    numero_programma = int(riga[n_index:t_index])
                    
                    # Extract the entire tool number after "T"
                    tool_number_match = re.search(r'T(\d+)', riga)
                    if tool_number_match:
                        tool_number_full = tool_number_match.group(1)
                        numero_torretta = int(tool_number_full[:-2])
                        numero_utensile = int(tool_number_full[-2:])
                        significato += f" - ricerca veloce Programma N{numero_programma} Cambio utensile a torretta {numero_torretta} usa correttore {numero_utensile}"
                    else:
                        significato += f" - Errore nell'estrazione del numero utensile"

                                        # Check for M5 in the line
                    if "M8" in riga:
                        significato += " - accende acqua"
                    if "M9" in riga:
                        significato += " - spegne acqua"
                    if "M5" in riga:
                        significato += " - Ferma mandrino"


                # Update the tool position for tool change commands
                if riga.startswith("N"):
                    precedente_comando_g = None  # Reset the previous G-code command for tool change

                elif comando in ["G04", "G4"] and parametri:
                    # Extract the numerical value after the X character
                    pause_duration_match = re.search(r'X(-?\d+(\.\d+)?)', ' '.join(parametri))
                    if pause_duration_match:
                        pause_duration = float(pause_duration_match.group(1))
                        significato += f" - Pausa di {pause_duration} secondi"

                elif comando in ["G96", "G97"] and parametri:
                    # G-codes for spindle speed control
                    velocita = converti_velocita_in_rpm(parametri[0].lstrip("S"))
                    significato += f" - Velocità del mandrino: {velocita} RPM"

                    # Check for spindle direction in the same line
                    spindle_direction = None
                    for param in parametri:
                        if param.startswith("M03") or param.startswith("M3"):
                            spindle_direction = "Orario"
                        elif param.startswith("M04") or param.startswith("M4"):
                            spindle_direction = "Antiorario"
                    if spindle_direction:
                        significato += f" - Accendi mandrino in senso {spindle_direction}"

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
    
                    #posizioni_percorso.append((posizione_attuale.get("X", 0), posizione_attuale.get("Y", 0), posizione_attuale.get("Z", 0)))
                    # Check if the command has an angle (A)
                    if "A" in param_dict:
                        angolo_attuale = float(param_dict["A"])
                        calcola_coordinate_con_angolo(posizione_attuale, angolo_attuale)
                        significato += f" - Posizione: (X={x}, Y={y}, Z={z}) - Angolo: {angolo_attuale} gradi (Coordinate aggiornate)"
                    else:
                        significato += f" - Posizione: (X={x}, Y={y}, Z={z})"

                    if comando in ["G00", "G0"]:
                        posizioni_finali_movimenti_rapidi.append((x, y, z))
                    else:
                        posizioni_finali_lavorazione.append((x, y, z))

                    # Se il comando corrente inizia con G, aggiorna la variabile del comando G precedente
                    if comando.startswith("G"):
                        precedente_comando_g = comando

                    # Check if the feed rate (F) is present in the parameters
                    feed_rate = param_dict.get("F", "N/D")
                    if feed_rate != "N/D":
                        significato += f" - Posizione: (X={x}, Y={y}, Z={z}), Velocità di avanzamento in lavorazione: {feed_rate}"
                    else:
                        significato += f" - Posizione: (X={x}, Y={y}, Z={z})"


                elif comando in ["G98", "G99"] and parametri:
                    # Check if the line contains G00, G0, G1, or G01
                    if any(cmd in riga for cmd in ["G1", "G01"]):
                        # Search for the letter F followed by the feed rate parameter
                        feed_rate_match = re.search(r'F(-?\d+(\.\d+)?)', riga)
                        feed_rate = float(feed_rate_match.group(1)) if feed_rate_match else "N/D"
                        # Search for values of X, Y, and Z parameters
                        x_match = re.search(r'X(-?\d+(\.\d+)?)', riga)
                        y_match = re.search(r'Y(-?\d+(\.\d+)?)', riga)
                        z_match = re.search(r'Z(-?\d+(\.\d+)?)', riga)

                        x_value = float(x_match.group(1)) if x_match else posizione_attuale.get("X", "N/D")
                        y_value = float(y_match.group(1)) if y_match else posizione_attuale.get("Y", "N/D")
                        z_value = float(z_match.group(1)) if z_match else posizione_attuale.get("Z", "N/D")

                        significato += f" - Feed Rate (velocità di avanzamento in lavorazione): {feed_rate}, Posizione: (X={x_value}, Y={y_value}, Z={z_value})"
                        posizioni_finali_lavorazione.append((x_value, y_value, z_value))
                       
                    elif any(cmd in riga for cmd in ["G00", "G0"]):
                        # Use the previous values if Z, X, or Y parameters are not present
                        x_match = re.search(r'X(-?\d+(\.\d+)?)', riga)
                        y_match = re.search(r'Y(-?\d+(\.\d+)?)', riga)
                        z_match = re.search(r'Z(-?\d+(\.\d+)?)', riga)
                        # Use previous values if the parameters are not present in the current line
                        x_value = float(x_match.group(1)) if x_match else posizione_attuale.get("X", "N/D")
                        y_value = float(y_match.group(1)) if y_match else posizione_attuale.get("Y", "N/D")
                        z_value = float(z_match.group(1)) if z_match else posizione_attuale.get("Z", "N/D")
                        significato += f" - Velocità di avanzamento controllata da operatore tramite tasti, Posizione: (X={x_value}, Y={y_value}, Z={z_value})"
                        posizioni_finali_movimenti_rapidi.append((x_value, y_value, z_value))

                    # Check for M5 in the line
                    if "M5" in riga:
                        significato += " - Ferma mandrino"




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
