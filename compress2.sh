#!/bin/bash

FOLDER="/pfad/zu/deinem/ordner"
OUTPUT="tokens.csv"

# Temporäre Datei für alle Tokens
TMPFILE=$(mktemp)

# Alle Textdateien durchgehen
find "$FOLDER" -type f | while read FILE; do
    # Prüfen, ob Datei textlich ist
    if file "$FILE" | grep -q "text"; then
        # Tokens zwischen Leerzeilen extrahieren
        awk 'BEGIN{RS=""; FS="[ \t\n]+"} {for(i=1;i<=NF;i++) print $i}' "$FILE"
    fi
done > "$TMPFILE"

# Token-Häufigkeit zählen und in CSV schreiben
echo "Token,Häufigkeit" > "$OUTPUT"
sort "$TMPFILE" | uniq -c | awk '{print $2 "," $1}' >> "$OUTPUT"

# Temporäre Datei löschen
rm "$TMPFILE"

echo "Fertig! Tokens und Häufigkeiten in $OUTPUT gespeichert."

