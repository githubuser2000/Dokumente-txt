#!/usr/bin/env bash
set -euo pipefail

pack_folder_to_single_file() {
    local folder="$1"
    local output="$2"
    : > "$output"

    find "$folder" -type f | while IFS= read -r file; do
        relpath="${file#$folder/}"
        size=$(stat -c%s "$file")
        printf "%s\n" "$relpath" >> "$output"
        printf "%s\n" "$size" >> "$output"
        cat "$file" >> "$output"
        printf "\n__NEXT__\n" >> "$output"
    done
    echo "__END__" >> "$output"
}

unpack_single_file() {
    local input="$1"
    local outdir="$2"
    mkdir -p "$outdir"
    exec 3<"$input"
    while true; do
        IFS= read -r -u 3 relpath || break
        [[ "$relpath" == "__END__" ]] && break
        IFS= read -r -u 3 size || break
        [[ -z "$relpath" || -z "$size" ]] && break

        outpath="$outdir/$relpath"
        mkdir -p "$(dirname "$outpath")"
        dd bs=1 count="$size" if=/dev/fd/3 of="$outpath" status=none
        # __NEXT__ trennt die Dateien
        IFS= read -r -u 3 marker || break
    done
    echo "Entpackt nach: $outdir"
}

if [[ $# -lt 3 ]]; then
    echo "Verwendung: $0 pack <ordner> <ausgabedatei>"
    echo "           $0 unpack <datei> <zielordner>"
    exit 1
fi

mode="$1"
src="$2"
tgt="$3"

case "$mode" in
    pack)   pack_folder_to_single_file "$src" "$tgt" ;;
    unpack) unpack_single_file "$src" "$tgt" ;;
    *) echo "Unbekannter Modus: $mode" >&2; exit 1 ;;
esac

