import random
from math import gcd
from functools import reduce

# Primfaktorzerlegung
def prime_factors(n: int) -> list[int]:
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors


# kgV (lcm) für zwei Zahlen
def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


# kgV für Liste
def lcm_list(values: list[int]) -> int:
    return reduce(lcm, values)


# Rationale Zahl kürzen
def reduce_rational(num: int, den: int) -> tuple[int, int]:
    g = gcd(num, den)
    return num // g, den // g


# Rationale Zahl anzeigen
def show_rational(num: int, den: int) -> str:
    n, d = reduce_rational(num, den)
    return f"{n}/{d}"


def main():
    # Zufallszahlen
    n1 = random.randint(10, 99)
    n2 = random.randint(10, 99)
    n3 = random.randint(10, 99)

    numbers = [n1, n2, n3]

    # Primfaktoren
    pf1 = prime_factors(n1)
    pf2 = prime_factors(n2)
    pf3 = prime_factors(n3)

    # ggT und kgV
    g12 = gcd(n1, n2)
    g23 = gcd(n2, n3)
    g13 = gcd(n1, n3)
    common = gcd(g12, n3)

    l = lcm_list(numbers)

    # Rationale Verhältnisse
    q1_num, q1_den = reduce_rational(n1, l)
    q2_num, q2_den = reduce_rational(n2, l)
    q3_num, q3_den = reduce_rational(n3, l)
    q4_num, q4_den = reduce_rational(common, l)

    labels = [
        "n1", "n2", "n3",
        "Primfaktoren n1",
        "Primfaktoren n2",
        "Primfaktoren n3",
        "ggT(n1,n2,n3)",
        "kgV",
        "n1/kgV",
        "n2/kgV",
        "n3/kgV",
        "ggT/kgV"
    ]

    values = [
        n1, n2, n3,
        pf1,
        pf2,
        pf3,
        common,
        l,
        show_rational(q1_num, q1_den),
        show_rational(q2_num, q2_den),
        show_rational(q3_num, q3_den),
        show_rational(q4_num, q4_den),
    ]

    for label, value in zip(labels, values):
        print(f"{label}: {value}")


if __name__ == "__main__":
    main()
