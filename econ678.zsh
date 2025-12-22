#!/usr/bin/env zsh

# Erzeuge eine zufällige Länge N >= 3
N=$(( (RANDOM % 20) + 3 ))

echo "Zufällige Länge: $N"

# Erzeuge N zufällige Fractions a/b
fractions=()
for ((i=1; i<=N; i++)); do
    a=$(( (RANDOM % 40) - 20 ))   # von -20 bis 19
    b=$(( (RANDOM % 9) + 1 ))     # von 1 bis 9
    fractions+="$a/$b"
done

echo "Fractions:"
printf "%s\n" "${fractions[@]}"
echo

# Funktion: berechnet 3D-Raum aus 3 Fractions
fraction_to_int() {
    echo $(( $1 ))   # Zsh wertet a/b automatisch als Integer Division aus
}

make_space_from_three() {
    f1=$1
    f2=$2
    f3=$3

    x=$(fraction_to_int $f1)
    y=$(fraction_to_int $f2)
    z=$(fraction_to_int $f3)

    # Beispiel: deterministische Achsenbildung
    # x_min = x
    # x_max = x + abs(y)
    # y_min = y
    # y_max = y + abs(z)
    # z_min = z
    # z_max = z + abs(x)

    abs_y=${y#-}
    abs_z=${z#-}
    abs_x=${x#-}

    x_min=$x
    x_max=$(( x + abs_y ))

    y_min=$y
    y_max=$(( y + abs_z ))

    z_min=$z
    z_max=$(( z + abs_x ))

    echo "$x_min $x_max $y_min $y_max $z_min $z_max"
}

echo "3D-Spaces:"
spaces=$(( N / 3 ))

for ((i=1; i<=spaces; i++)); do
    idx=$(( (i-1)*3 ))
    f1=${fractions[$((idx+1))]}
    f2=${fractions[$((idx+2))]}
    f3=${fractions[$((idx+3))]}

    printf "Fractions %s %s %s  →  3D-Space: " "$f1" "$f2" "$f3"
    make_space_from_three $f1 $f2 $f3
done

