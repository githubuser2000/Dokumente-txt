#!/bin/bash
# rle_encode.sh
# Kodiert eine Zeichenkette mit Run-Length-Encoding (RLE)

input="$1"  # Eingabe als Argument, z.B.: ./rle_encode.sh "AAAAABBBBCCCCCCDD"

if [ -z "$input" ]; then
    echo "Usage: $0 <string>"
    exit 1
fi

prev=""
count=0
encoded=""

for (( i=0; i<${#input}; i++ )); do
    char="${input:$i:1}"
    if [ "$char" == "$prev" ]; then
        ((count++))
    else
        if [ "$prev" != "" ]; then
            encoded+="${prev}${count}"
        fi
        prev="$char"
        count=1
    fi
done

# letztes Token anhängen
encoded+="${prev}${count}"

echo "$encoded"
