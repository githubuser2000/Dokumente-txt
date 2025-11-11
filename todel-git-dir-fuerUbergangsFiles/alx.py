#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import sys

def main():
    # Endlosschleife, um kontinuierlich Eingaben zu verarbeiten
    while True:
        # Liest eine Zeile von der Standardeingabe
        input_data = sys.stdin.readline()
        
        # Überprüft, ob die Eingabe leer ist (Ende des Streams)
        if not input_data:
            break

        # Verändert die eingelesenen Daten leicht
        modified_data = input_data.strip() + " - bearbeitet"

        # Gibt die veränderten Daten an die Standardausgabe zurück
        print(modified_data)
        sys.stdout.flush()  # Flusht die Ausgabe, damit sie sofort sichtbar ist

if __name__ == "__main__":
    main()
