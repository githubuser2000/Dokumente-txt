#!/bin/bash

FOLDER="/pfad/zu/deinem/ordner"
OUTPUT="tokens.csv"

# Leere Datei erstellen oder überschreiben
> "$OUTPUT"

# Alle Dateien im Ordner durchgehen
find "$FOLDER" -type f | while read FILE; do
    # Prüfen, ob Datei textlich ist
    if file "$FILE" | grep -q "text"; then
        # Tokens zwischen Leerzeilen extrahieren
        awk 'BEGIN{RS=""; FS="[ \t\n]+"} {for(i=1;i<=NF;i++) print $i}' "$FILE" >> "$OUTPUT"
    fi
done

echo "Fertig! Tokens gespeichert in $OUTPUT"

