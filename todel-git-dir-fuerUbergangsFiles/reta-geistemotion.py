#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import sys
from collections import OrderedDict

sys.path.insert(0, "/home/alex/myRepos/reta")


def couldBePrimeNumberPrimzahlkreuz(num: int) -> bool:
    Under24 = (1, 5, 7, 11, 13, 17, 19, 23)
    return num % 24 in Under24


def couldBePrimeNumberPrimzahlkreuz_fuer_innen(num: int) -> bool:
    Under24 = (5, 11, 17, 23)
    return num % 24 in Under24


def couldBePrimeNumberPrimzahlkreuz_fuer_aussen(num: int) -> bool:
    Under24 = (1, 7, 13, 19)
    return num % 24 in Under24


def primfaktoren(n):

    """zerlegt eine Zahl in ihre Primfaktoren

    >>> primfaktoren(24)
    [2, 2, 2, 3]

    """

    faktoren = []
    z = n
    while z > 1:
        # bestimme den kleinsten Primfaktor p von z
        i = 2
        gefunden = False
        while i * i <= n and not gefunden:
            if z % i == 0:
                gefunden = True
                p = i
            else:
                i = i + 1
        if not gefunden:
            p = z
        # füge p in die Liste der Faktoren ein
        faktoren = faktoren + [p]
        z = z // p
    return faktoren


def primRepeat(n):
    n.reverse()
    c = 1
    b = None
    d = []
    for a in n:
        if b == a:
            c += 1
        else:
            c = 1
        d += [[a, c]]
        b = a
    d.reverse()
    b = None
    f = []
    for e, g in d:
        if b != e:
            if g == 1:
                f += [e]
            else:
                f += [str(e) + "^" + str(g)]
        b = e

    return f


zahl = sys.argv[1]
if zahl.isdecimal():
    zahl = int(zahl)
    prFa = primfaktoren(zahl)
    # print("Faktoren: {}".format(prFa))
    auss = [couldBePrimeNumberPrimzahlkreuz_fuer_aussen(a) for a in prFa]
    # print("außen: {}".format(auss))
    innen = [couldBePrimeNumberPrimzahlkreuz_fuer_innen(a) for a in prFa]
    # print("innen: {}".format(innen))
    zwei = len([a for a in prFa if a == 2])
    # print("zwei: {}".format(zwei))
    gefuehl = any(auss)
    denken = any(innen)
    # anZahlInnen = len([a for a in innen if True])
    totalTopologie = zwei > 1 and gefuehl
    etwasTopologie = (zwei > 1 or (zwei > 0 and gefuehl)) and not totalTopologie
    totalMaterie = zwei > 4
    etwasMaterie = zwei == 4
    wenigMaterie = zwei == 3
    kaumMaterie = zwei == 2
    x, y, z = denken, (2 in prFa), (3 in prFa)
    totalEnerge = x and y and z
    einermassenEnergie = ((x and y) or (y and z) or (y and z)) and not totalEnerge
    kaumEnergie = not einermassenEnergie and not totalEnerge and (x or y or z)
    ausgabeStringList = []
    if denken:
        ausgabeStringList += ["eine Denkart"]
    if gefuehl:
        ausgabeStringList += ["eine Gefühlsart"]
    if totalMaterie:
        ausgabeStringList += ["total Materie"]
    if totalTopologie:
        ausgabeStringList += ["total eine Art Topologie"]
    if totalEnerge:
        ausgabeStringList += ["total eine Energie-Art"]
    if etwasTopologie:
        ausgabeStringList += ["etwas eine Art Topologie"]
    if etwasMaterie:
        ausgabeStringList += ["etwas eine Art Materie"]
    if wenigMaterie:
        ausgabeStringList += ["wenig eine Art Materie"]
    if einermassenEnergie:
        ausgabeStringList += ["einigermaßen eine Energie-Art"]
    if kaumEnergie:
        ausgabeStringList += ["kaum eine Energie-Art"]
    if kaumMaterie:
        ausgabeStringList += ["kaum eine Materie-Art"]
    ausgabeString = "; ".join(ausgabeStringList)
    print(ausgabeString)
