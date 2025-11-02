#!/usr/bin/env python3
import os
import struct

def pack_folder_to_single_file(folder_path, output_file):
    with open(output_file, 'wb') as out:
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                file_path = os.path.join(root, name)
                rel_path = os.path.relpath(file_path, folder_path).encode('utf-8')
                size = os.path.getsize(file_path)

                # Header: [Länge des Pfads (4 Bytes)] [Pfad] [Dateigröße (8 Bytes)] [Dateidaten]
                out.write(struct.pack('<I', len(rel_path)))
                out.write(rel_path)
                out.write(struct.pack('<Q', size))

                with open(file_path, 'rb') as f:
                    while chunk := f.read(65536):
                        out.write(chunk)

        # Endmarkierung (Pfadlänge = 0)
        out.write(struct.pack('<I', 0))
    print(f"Fertig: {output_file}")

def unpack_single_file(input_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with open(input_file, 'rb') as f:
        while True:
            # Pfadlänge lesen
            data = f.read(4)
            if not data:
                break
            path_len = struct.unpack('<I', data)[0]
            if path_len == 0:
                break

            rel_path = f.read(path_len).decode('utf-8')
            size = struct.unpack('<Q', f.read(8))[0]
            out_path = os.path.join(output_folder, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            with open(out_path, 'wb') as out:
                remaining = size
                while remaining > 0:
                    chunk = f.read(min(65536, remaining))
                    if not chunk:
                        raise IOError("Unerwartetes Dateiende")
                    out.write(chunk)
                    remaining -= len(chunk)

    print(f"Entpackt nach: {output_folder}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Alle Dateien eines Ordners in einer Datei speichern oder wiederherstellen.")
    parser.add_argument("mode", choices=["pack", "unpack"], help="pack = zusammenführen, unpack = wiederherstellen")
    parser.add_argument("source", help="Ordner (bei pack) oder Datei (bei unpack)")
    parser.add_argument("target", help="Zieldatei (bei pack) oder Zielordner (bei unpack)")
    args = parser.parse_args()

    if args.mode == "pack":
        pack_folder_to_single_file(args.source, args.target)
    else:
        unpack_single_file(args.source, args.target)

