#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import sys
import time

def run_daemon():
    # Endlosschleife, um kontinuierlich Eingaben zu verarbeiten
    while True:
        # Liest eine Zeile von der Standardeingabe
        input_data = sys.stdin.readline()

        # Wenn keine Eingabe kommt, kurz warten und dann weitermachen
        if not input_data:
            time.sleep(0.1)
            continue

        # Verändert die eingelesenen Daten leicht
        modified_data = input_data.strip() + " - bearbeitet"

        # Gibt die veränderten Daten an die Standardausgabe zurück
        print(modified_data)
        sys.stdout.flush()  # Flusht die Ausgabe sofort

if __name__ == "__main__":
    run_daemon()
