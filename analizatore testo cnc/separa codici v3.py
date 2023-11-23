import re

# Apri il file in modalità lettura
with open('CNC.txt', 'r') as file:
    # Leggi tutte le righe del file
    lines = file.readlines()

# Apri il file in modalità scrittura sovrascrivendo il contenuto
with open('CNC.txt', 'w') as file:
    # Itera attraverso ogni riga
    for line in lines:
        # Controlla se la riga inizia con i pattern da riconoscere
        if line.startswith("0032"):
            file.write("Program Number: " + line)
        elif line.startswith("z&HE:%"):
            file.write("Connection Command: " + line)
        else:
            # Cerca una corrispondenza usando espressioni regolari
            matches = re.finditer(r'([A-Z]+)(\d+)', line)
            
            # Se ci sono corrispondenze, modifica la riga
            if matches:
                for match in matches:
                    # Modifica la riga aggiungendo spazi tra il codice e i valori numerici
                    modified_line = match.group(1) + ''.join(match.group(2)) + ' '
                    file.write(modified_line)
            else:
                # Se non ci sono corrispondenze, scrivi la riga originale nel file
                file.write(line)
