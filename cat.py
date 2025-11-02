#!/usr/bin/env python3
import sys
import os

def cat_file(f):
    try:
        # lese/schreibe im Binary-Mode, so verhält sich cat korrekt auch bei Binärdateien
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
    except BrokenPipeError:
        # z.B. wenn Ausgabe in `head` gepiped wurde und vorzeitig schließt
        sys.exit(0)

def main():
    args = sys.argv[1:]
    if not args:
        # keine Dateien => von stdin lesen
        cat_file(sys.stdin.buffer)
    else:
        for name in args:
            if name == "-":
                cat_file(sys.stdin.buffer)
            else:
                try:
                    with open(name, "rb") as f:
                        cat_file(f)
                except OSError as e:
                    # Fehler mimimale Ausgabe an stderr wie /bin/cat
                    sys.stderr.write(f"cat: {name}: {e.strerror}\n")

if __name__ == "__main__":
    main()

