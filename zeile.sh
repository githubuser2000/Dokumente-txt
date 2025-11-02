#!/bin/bash

# Prüfe, ob eine Zeilennummer übergeben wurde
if [ -z "$1" ]; then
    echo "Usage: $0 <zeilennummer>" >&2
    exit 1
fi

ziel=$(( $1 + 1 ))
# Gebe nur die angegebene Zeile aus
awk "NR==$ziel"

