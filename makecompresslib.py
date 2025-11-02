import os
import csv

# Pfad zum Ordner mit den Dateien
folder_path = "/pfad/zu/deinem/ordner"
output_csv = "tokens.csv"

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except:
        return False

def extract_tokens_from_file(file_path):
    tokens = []
    with open(file_path, 'r', encoding='utf-8') as f:
        block = []
        for line in f:
            line = line.strip()
            if line == "":  # Leerzeile → Block beendet
                if block:
                    tokens.extend(" ".join(block).split())
                    block = []
            else:
                block.append(line)
        if block:  # Letzter Block
            tokens.extend(" ".join(block).split())
    return tokens

all_tokens = []

for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        if is_text_file(file_path):
            all_tokens.extend(extract_tokens_from_file(file_path))

# CSV schreiben
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for token in all_tokens:
        writer.writerow([token])

print(f"Gespeichert {len(all_tokens)} Tokens in {output_csv}")

