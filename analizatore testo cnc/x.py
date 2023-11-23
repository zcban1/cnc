def trasforma_stringa(input_string):
    if input_string.startswith("X"):
        numero_dopo_x = input_string[len("X26.042"):].strip()
        if numero_dopo_x:  # Verifica se il numero dopo "X26.042" non è vuoto
            return f"X={numero_dopo_x}"
    return input_string

# Esempio di utilizzo:
input_string = "X26.042"
output_string = trasforma_stringa(input_string)
print(output_string)

