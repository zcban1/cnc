import re

# Apri il file in modalità lettura
with open('CNC.txt', 'r') as file:
    # Leggi tutte le righe del file
    lines = file.readlines()

# Apri un nuovo file in modalità scrittura
with open('CNC_modificato.txt', 'w') as new_file:
    # Itera attraverso ogni riga
    for line in lines:
        if line.startswith(":0032"):
            new_file.write("Program Number: " + line)
        elif line.startswith("z&HE:%"):
            new_file.write("Connection Command: " + line)
        else:
            matches = re.finditer(r'([A-Z]+[+-]?\d*\.?\d*|\([^)]*\))', line)            # Se ci sono corrispondenze, modifica la riga
            if matches:
                for match in matches:
                    # Modifica la riga aggiungendo spazi tra il codice e i valori numerici
                    modified_line = match.group(1) + ' '
                    new_file.write(modified_line)
            else:
                # Se non ci sono corrispondenze, scrivi la riga originale nel nuovo file
                new_file.write(line)

            # Aggiungi un carattere di nuova riga dopo ciascuna riga nel nuovo file
            new_file.write('\n')
