#!/usr/bin/env bash

# Log-Datei
LOG_FILE="$HOME/clipboard.log"

# Intervall in Sekunden
INTERVAL=2

# letzte Hash merken
LAST_HASH=""

# Prüfen, ob wl-paste vorhanden ist
if ! command -v wl-paste &> /dev/null; then
    echo "wl-paste nicht gefunden. Bitte installieren."
    exit 1
fi

while true; do
    # Clipboard-Inhalt auslesen
    CONTENT=$(wl-paste -n 2>/dev/null)

    # Hash berechnen
    CURRENT_HASH=$(echo -n "$CONTENT" | sha256sum | awk '{print $1}')

    # Wenn Hash sich geändert hat und Inhalt nicht leer
    if [[ "$CURRENT_HASH" != "$LAST_HASH" && -n "$CONTENT" ]]; then
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP]" >> "$LOG_FILE"
        echo "$CONTENT" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"

        # Optional: Ausgabe im Terminal
        echo "Neuer Clipboard-Inhalt geloggt: ${CONTENT:0:30}..."

        LAST_HASH="$CURRENT_HASH"
    fi

    sleep "$INTERVAL"
done

