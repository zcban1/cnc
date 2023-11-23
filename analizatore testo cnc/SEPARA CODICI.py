import re

# Apri il file in modalità lettura
with open('CNC.txt', 'r') as file:
    # Leggi tutte le righe del file
    lines = file.readlines()

# Apri il file in modalità scrittura sovrascrivendo il contenuto
with open('CNC.txt', 'w') as file:
    # Itera attraverso ogni riga
    for line in lines:
        # Cerca una corrispondenza usando espressioni regolari
        matches = re.finditer(r'([A-Z]+)(\d+)', line)
        
        # Se ci sono corrispondenze, modifica la riga
        for match in matches:
            modified_line = match.group(1) + ' '.join(match.group(2)) + ' '
            file.write(modified_line)
        
        # Se non ci sono corrispondenze, scrivi la riga originale nel file
        if not matches:
            file.write(line)


