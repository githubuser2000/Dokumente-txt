#!/bin/bash
if [ $# -eq 0 ]; then
    # von stdin lesen
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done
else
    for f in "$@"; do
        if [ "$f" = "-" ]; then
            while IFS= read -r line; do
                printf '%s\n' "$line"
            done
        else
            while IFS= read -r line <&3; do
                printf '%s\n' "$line"
            done 3<"$f"
        fi
    done
fi

