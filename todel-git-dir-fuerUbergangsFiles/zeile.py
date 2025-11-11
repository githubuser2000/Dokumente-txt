#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <zeilennummer>", file=sys.stderr)
    sys.exit(1)

try:
    zeile = int(sys.argv[1])
except ValueError:
    print("Fehler: Zeilennummer muss eine Zahl sein.", file=sys.stderr)
    sys.exit(1)
ziel = zeile + 1

for index, line in enumerate(sys.stdin, start=1):
    if index == ziel:
        print(line.rstrip('\n'))
        break
