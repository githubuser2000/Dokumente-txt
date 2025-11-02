#!/bin/bash
# rle_decode.sh
# Dekodiert eine RLE-kodierte Zeichenkette

input="$1"

if [ -z "$input" ]; then
    echo "Usage: $0 <encoded_string>"
    exit 1
fi

decoded=""
symbol=""
count=""

for (( i=0; i<${#input}; i++ )); do
    char="${input:$i:1}"
    if [[ "$char" =~ [0-9] ]]; then
        count+="$char"
    else
        if [ -n "$symbol" ] && [ -n "$count" ]; then
            decoded+=$(printf "%0.s$symbol" $(seq 1 $count))
        fi
        symbol="$char"
        count=""
    fi
done

# letztes Symbol ausgeben
if [ -n "$symbol" ] && [ -n "$count" ]; then
    decoded+=$(printf "%0.s$symbol" $(seq 1 $count))
fi

echo "$decoded"
