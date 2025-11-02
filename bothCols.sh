#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 file1.csv file2.csv col1 col2"
    exit 1
fi

file1="$1"
file2="$2"
col1="$3"
col2="$4"

term_width=$(tput cols)

# CSV-Spalten auslesen
mapfile -t col1_data < <(awk -F, -v c="$col1" '{print $c}' "$file1")
mapfile -t col2_data < <(awk -F, -v c="$col2" '{print $c}' "$file2")

# Länge angleichen
len1=${#col1_data[@]}
len2=${#col2_data[@]}
max_len=$(( len1 > len2 ? len1 : len2 ))
for ((i=len1; i<max_len; i++)); do col1_data[i]=""; done
for ((i=len2; i<max_len; i++)); do col2_data[i]=""; done

width_num=4
width1=0
width2=0
for s in "${col1_data[@]}"; do (( ${#s} > width1 )) && width1=${#s}; done
for s in "${col2_data[@]}"; do (( ${#s} > width2 )) && width2=${#s}; done

# Prüfen ob alles in Terminal passt
total_width=$((width_num + 3 + width1 + 3 + width2))
if (( total_width > term_width )); then
    ratio=$(awk "BEGIN{print ($term_width-6)/($width_num+$width1+$width2)}")
    width1=$(awk "BEGIN{w=int($width1*$ratio); print (w>0?w:1)}")
    width2=$(awk "BEGIN{w=int($width2*$ratio); print (w>0?w:1)}")
fi

# Ausgabe
for ((i=0; i<max_len; i++)); do
    # Zeilennummer
    if (( i+1 == 0 )); then
        num_str="    "
    else
        num_str=$(printf "%04d" $((i+1)))
    fi

    # Wrap der CSV-Spalten, Zeilennummer NICHT folden
    readarray -t lines1 < <(echo "${col1_data[i]}" | fold -w $width1)
    readarray -t lines2 < <(echo "${col2_data[i]}" | fold -w $width2)

    # Zeilenhöhe angleichen
    max_lines=${#lines1[@]}
    (( ${#lines2[@]} > max_lines )) && max_lines=${#lines2[@]}

    for ((j=0; j<max_lines; j++)); do
        c1="${lines1[j]:-}"
        c2="${lines2[j]:-}"
        if (( j == 0 )); then
            printf "%-4s | %-*s | %-*s\n" "$num_str" "$width1" "$c1" "$width2" "$c2"
        else
            printf "    | %-*s | %-*s\n" "$width1" "$c1" "$width2" "$c2"
        fi
    done
done

