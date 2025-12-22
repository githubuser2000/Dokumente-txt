#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fractions import Fraction
from math import prod, gcd, atan, pi, degrees
import random
from functools import reduce
import operator
# Primfaktorzerlegung
def prime_factors(n):
    i = 2
    factors = []
    while i*i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

# Zufällige Auswahl von 3 unterschiedlichen Zahlen >1 mit verschiedenen Primfaktoren
def generate_three_unique(max_val=42):
    def ng():
        return prime_factors(random.randint(3, max_val))

    while True:
        n1, n2, n3 = ng(), ng(), ng()
        if n1 != n2 and n1 != n3 and n2 != n3 and (set(n1) & set(n2) & set(n3) not in ({},{1},{0})):
            p1, p2, p3 = reduce(operator.mul,n1,1), reduce(operator.mul,n2,1), reduce(operator.mul,n3,1)
            common = reduce(gcd, {p1, p2, p3})
            if common < 3:
                continue
            return p1, p2, p3, common

# Ausführung
try:
    gen3 = lambda m=42: next(                                                                  (p1,p2,p3,c)                                                                           for n1,n2,n3 in [(pf(random.randint(3,m)), pf(random.randint(3,m)), pf(random.randint(3,m)))]                                                                                 if len({tuple(n1), tuple(n2), tuple(n3)}) == 3                                         and (c:=reduce(gcd,[prod(n) for n in [n1,n2,n3]])) >= 3                                for p1,p2,p3 in [(prod(n1), prod(n2), prod(n3))]                                   )

    n1, n2, n3, common = gen3()
except:
    n1, n2, n3, common = generate_three_unique()
print("zufällig Generierte 3 unterschiedliche Zahlen mit unterschiedlichen Primfaktorzerlegungen:", n1, n2, n3, "verwandt " , common)
# Bildung rationaler Zahl
def Q(a, b):
    return Fraction(a, b)
q1 = Q(n1, n2)
q2 = Q(n2, n3)
q3 = Q(q1, q2)
q4 = Q(q2, q1)

# Gesamte Menge: 7 Zahlen
S = [n1, n2, n3, common, q1, q2, q3, q4]
# Generator zur Beschriftung der 7 Zahlen
def label_generator(values):
    labels = [
        "Wert Geld Währung Nummer Zahlen Wert Währung (folgende sind Währungen von nicht Nummern Zahlen Werten)",
        "Gutartigkeit Selbstlosigkeit Führungsschicht Regierung Herrschaft",
        "Ganzheit Kaputtheit Nicht-Armut Zentralität Unterschicht",
        "Primfaktor-Zerlegungs-Verwandschafts-Gemeinsamkeit dreier positiver zufälliger ganzer Natürlicher Zahlen Zahl",
        "Verhältnis Wert zu Führungsschicht, Gutartigkeit Produkt, Firma, Leistung als Winkel-Richtung",
        "Wert Verhältnis zu Unterschicht, Kaputtheit Armut Ganzheit Gesundheit zum Wert statt ins Verhältnis eine Skalierung",
        "Führungsschicht Regierer Parteien gegenüber Unterschicht Relation Verhältnis oder als Skarierung gemeint und zu verstehen, entweder oder",
        "Unterschicht Verhältnis zu Führungsschicht Regierung Herrscher Relation Verhältnis, oder als Skarierung gemeint und zu verstehen, entweder oder"

    ]
    for label, value in zip(labels, S):
        yield label, value

for l, v in label_generator(S):
    print(f"{l}: {v}")

# --- Zusatz: Winkelabbildung für die vier rationalen Zahlen ------------------

def angle(f: Fraction):
    """Berechnet θ = 2*atan(f) in (rad, grad)."""
    x = float(f)
    theta_rad = 2 * atan(x)
    theta_deg = degrees(theta_rad)
    return theta_rad, theta_deg

# Vier Winkel berechnen
a1 = angle(q1)
a2 = angle(q2)
a3 = angle(q3)
a4 = angle(q4)

print("\n--- Winkel der vier rationalen Zahlen ---")
print(f"q1 = {q1}  →  θ = {a1[0]:.2f} rad = {a1[1]:.2f}°")
print(f"q2 = {q2}  →  θ = {a2[0]:.2f} rad = {a2[1]:.2f}°")
print(f"q3 = {q3}  →  θ = {a3[0]:.2f} rad = {a3[1]:.2f}°")
print(f"q4 = {q4}  →  θ = {a4[0]:.2f} rad = {a4[1]:.2f}°")

print("\n--- Beziehung q ↔ 1/q (orthogonal = -180°) ---")
print(f"θ(q1) - θ(q2) = {a1[1] - a2[1]:.2f}°")
print(f"θ(q3) - θ(q4) = {a3[1] - a4[1]:.2f}°")

# 8 Skalierungsfaktoren
SCALE = [
    q1,
    q2,
    q3,
    q4,
    1/q1,
    1/q2,
    1/q3,
    1/q4,
]

# Auf n1, n2, n3 anwenden
scaled = [
    (s, float(s*n1), float(s*n2), float(s*n3))
    for s in SCALE
]

print("\n--- Skalierungen auf n1, n2, n3 ---")
for s, a, b, c in scaled:
    print(f"Skalierung {s}  →  n1'={a:.1f}, n2'={b:.1f}, n3'={c:.1f}")
