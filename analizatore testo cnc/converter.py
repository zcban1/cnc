import re


def modifica_file_cnc(input_file, output_file):
    # Apri il file in modalità lettura
    with open(input_file, 'r') as file:
        # Leggi tutte le righe del file
        lines = file.readlines()

    # Apri un nuovo file in modalità scrittura
    with open(output_file, 'w') as new_file:
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

def aggiungi_comando_g_spazio(input_file):
    with open(input_file, 'r+') as file:
        lines = file.readlines()  # Leggi tutte le righe nel file
        file.seek(0)  # Torna all'inizio del file

        current_command = None  # Memorizza l'ultimo comando letto

        for i, riga in enumerate(lines):
            # Controlla se la riga inizia con "G" o "A"
            if riga.startswith(('G1', 'G01', 'G00', 'G0')):
                # Memorizza solo il comando "G1" o "G0" dalla riga corrente
                current_command = riga.split()[0]
            elif riga.startswith(('X', 'Z', 'Y', 'A')):
                # Se la riga non inizia con 'G1', 'G01', 'G00', 'G0, aggiungi solo il comando corrente seguito da uno spazio alla riga corrente
                if current_command:
                    lines[i] = f"{current_command} {riga}"  # Aggiungi il comando seguito da uno spazio alla riga
            else:
                continue

        # Scrivi le righe modificate nel file
        file.seek(0)
        file.writelines(lines)
        file.truncate()




