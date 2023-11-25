import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import math
from disegna_pezzo import plot_cnc_profile_2d,plot_cnc_profile
from vocabolario import comandi_cnc
from converter import  aggiungi_comando_g_spazio,modifica_file_cnc


precedente_comando_g = None  # Inizializza la variabile per il comando G precedente

def converti_velocita_in_rpm(velocita):
    try:
        return int(velocita)
    except ValueError:
        return "N/D"

def calcola_coordinate_con_angolo(posizione_attuale, angolo):
    # Calcola nuove coordinate basate sull'angolo
    if 'X' in posizione_attuale and 'Y' in posizione_attuale:
        x_originale = posizione_attuale['X']
        y_originale = posizione_attuale['Y']
        
        # Converti l'angolo in radianti
        angolo_rad = math.radians(angolo)
        
        # Calcola nuove coordinate basate sull'angolo
        x_nuovo = x_originale * math.cos(angolo_rad) - y_originale * math.sin(angolo_rad)
        y_nuovo = x_originale * math.sin(angolo_rad) + y_originale * math.cos(angolo_rad)
        
        # Aggiorna le coordinate nella posizione attuale
        posizione_attuale['X'] = x_nuovo
        posizione_attuale['Y'] = y_nuovo

def calcola_coordinate_con_raggio_lineare(posizione_attuale, raggio, z_destinazione):
    # Estrai le coordinate correnti
    x_corrente = posizione_attuale.get("X", 0.0)
    y_corrente = posizione_attuale.get("Y", 0.0)
    z_corrente = posizione_attuale.get("Z", 0.0)

    # Calcola la lunghezza orizzontale del movimento
    lunghezza_orizzontale = math.sqrt(raggio**2 - (z_destinazione - z_corrente)**2)

    # Calcola le nuove coordinate
    nuovo_x = x_corrente + lunghezza_orizzontale
    nuovo_y = y_corrente

    # Aggiorna la posizione attuale
    return nuovo_x, nuovo_y, z_destinazione

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

                    # Check for M in the line
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
                        significato += f" - Velocità di avanzamento in lavorazione: {feed_rate}"

                    # Check if the radius (R) is present in the parameters for G1 command
                    if comando in ["G01", "G1"] and "R" in param_dict:
                        raggio = float(param_dict.get("R", 0.0))
                        if raggio != 0.0:
                            # Calcola le nuove coordinate in base al raggio
                            nuovo_x, nuovo_y, nuovo_z = calcola_coordinate_con_raggio_lineare(posizione_attuale, raggio, z)
                            # Aggiorna le coordinate nella posizione attuale
                            posizione_attuale.update({"X": nuovo_x, "Y": nuovo_y, "Z": nuovo_z})
                            # Aggiorna il significato con le informazioni sul raggio
                            significato += f" - Raggio: {raggio} (Coordinate aggiornate)"

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


if __name__ == "__main__":
    input_filename = 'CNC.txt'
    output_filename = 'CNC_modificato.txt'
    file_modificato = output_filename
    modifica_file_cnc(input_filename, output_filename)
    aggiungi_comando_g_spazio(file_modificato)
    nome_file_cnc = output_filename
    posizioni_percorso,  posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti  = analizza_file_cnc(nome_file_cnc)
    # Stampa i commenti nello stesso numero di righe del file
    print("\nCommenti:")
    for commento in commenti:
        print(commento)
    plot_cnc_profile_2d(posizioni_percorso, posizioni_finali_movimenti_rapidi, posizioni_finali_lavorazione, commenti)
