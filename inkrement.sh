#!/bin/bash

start_val=""
count=0
declare -A val_counter

while read -r line; do
    if [[ $line =~ ^([0-9]{4}) ]]; then
        num="${BASH_REMATCH[1]}"
        [[ -z "$start_val" ]] && start_val="$num"
        ((count++))

        prefix="${num:0:2}"  # z.B. 1010 → 10
        ((val_counter[$prefix]++))

        echo "Zeile $count: Start=$start_val, Aktuelle=$num, Gruppe=$prefix, Vorkommen=${val_counter[$prefix]}"
    fi
done

