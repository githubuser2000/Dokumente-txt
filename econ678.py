#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from fractions import Fraction

def random_fraction_list(min_len=3, max_len=18):
    """Erzeugt eine zufällige Liste aus ints und Fractions."""
    length = random.randint(min_len, max_len)
    values = []
    for _ in range(length):
        if random.random() < 0.5:
            n = random.randint(1, 9)
            d = random.randint(1, 9)
            values.append(Fraction(n, d))
        else:
            values.append(random.randint(1, 20))
    return values


def fraction_triplet_to_space(f1, f2, f3):
    """3 Fractions → 6 ints (ein 3D Space)."""
    ints = []
    for f in (f1, f2, f3):
        val = int(f * 10) if isinstance(f, Fraction) else int(f)
        minv = val
        maxv = max(val * 2, val)  # mindestens val selbst, maximal doppelte Länge
        ints.extend([minv, maxv])
    return tuple(ints)


def fractions_to_spaces(values):
    """Aus beliebig vielen Fraction/Int-Werten:
       alle 3er-Blöcke erzeugen jeweils einen eigenen 3D Space."""
    if len(values) < 3:
        raise ValueError("Mindestens 3 Werte benötigt")

    spaces = []
    # gruppiere immer 3 Werte zu einem eigenen 3D Space
    for i in range(0, len(values) - (len(values) % 3), 3):
        f1, f2, f3 = values[i:i+3]
        space = fraction_triplet_to_space(f1, f2, f3)
        spaces.append(space)

    return spaces


# ------- Testlauf ---------

fractions_list = random_fraction_list()
print("Liste:", fractions_list)

spaces = fractions_to_spaces(fractions_list)
print("3D Spaces:")
for s in spaces:
    print(s)

