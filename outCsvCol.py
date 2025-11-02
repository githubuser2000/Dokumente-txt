import csv
import sys
def spalte_aus_csv_ausgeben(dateiname, spaltennummer):
    try:
        with open(dateiname, newline='\n', encoding='utf-8') as csvdatei:
            reader = csv.reader(csvdatei, delimiter=';')
            merkezeile = sum(1 for _ in reader)
        with open(dateiname, newline='\n', encoding='utf-8') as csvdatei:
            reader = csv.reader(csvdatei, delimiter=';')
            for i, zeile in enumerate(reader):
                ifa, ifb = spaltennummer < len(zeile), len(zeile[spaltennummer].strip()) > 3
                if ifa and ifb:
                    merkezeile = i+1

        with open(dateiname, newline='\n', encoding='utf-8') as csvdatei:
            reader = csv.reader(csvdatei, delimiter=';')
            for i, zeile in enumerate(reader):
                ifa, ifb, ifc = spaltennummer < len(zeile), len(zeile[spaltennummer].strip()) > 3, merkezeile > i
                if ifa and ifc:
                    print(f"{i}.:   {zeile[spaltennummer]}")
                elif ifa and ifc:
                    print(f"{i}.")
                else:
                    #print(f"[WARNUNG] Zeile zu kurz: {zeile}")
                    break
    except FileNotFoundError:
        print(f"[FEHLER] Datei nicht gefunden: {dateiname}")
    except Exception as e:
        print(f"[FEHLER] {e}")

def start():
    if len(sys.argv) != 3:
        print("Verwendung: pypy3 spalte_auslesen.py <dateiname.csv> <spaltennummer>")
        sys.exit(1)

    dateiname = sys.argv[1]
    try:
        spaltennummer = int(sys.argv[2])
    except ValueError:
        print("[FEHLER] Die Spaltennummer muss eine Ganzzahl sein.")
        sys.exit(1)

    spalte_aus_csv_ausgeben(dateiname, spaltennummer)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: pypy3 spalte_auslesen.py <dateiname.csv> <spaltennummer>")
        sys.exit(1)

    dateiname = sys.argv[1]
    try:
        spaltennummer = int(sys.argv[2])
    except ValueError:
        print("[FEHLER] Die Spaltennummer muss eine Ganzzahl sein.")
        sys.exit(1)

    spalte_aus_csv_ausgeben(dateiname, spaltennummer)
