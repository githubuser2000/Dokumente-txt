#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
from collections import OrderedDict


def grKl(A: set, B: set) -> tuple[set, set]:
    """
    Gibt 2 Mengen zurück: eine Menge aus allem, das größer ist als im ersten Parameter aus dem zweiten Parameter
    und in die zweite Menge kommt alles, das kleiner ist, als in der ersten Menge aus der zweiten Menge
    """
    C = set()
    D = set()
    if len(B) == 0:
        return A, A
    for a in A:
        if a > max(B):
            C.add(a)
        elif a < min(B):
            D.add(a)
    return C, D


def getDictLimtedByKeyList(d: dict, keys) -> dict:
    """
    Gibt ein dict zurück, das aus einem dict gebildet wird, aber davon nur das nimmt, was an mehreren keys genommen werden soll.
    """
    return OrderedDict({k: d[k] for k in keys if k in d})


def bruchSpalt(text) -> list:
    """
    Gibt eine Liste aus Tupeln zurück, die entweder einen bis mehrere oder zwei Werte enthalten.
    Eingabe sind Brüche gemischt mit Textwerten
    Das Ergebnis bei zwei Werten ist der Bruch
    Bei ein bis mehreren Werten, also auch 2 handelt es sich um die Textwerte, welche zwischen den Brüchen waren.
    Die Reihenfolge vom Ergebnis ist die Gleiche, wie bei dem Eingabe-Text
    """
    bruchSpalten: list[str] = text.split("/")
    bruchSpaltenNeu = []
    bruchSpaltenNeu2 = []
    if len(bruchSpalten) < 2:
        """Ein Bruch hat immer mindestens 2 Zahlen"""
        return []
    keineZahl = OrderedDict()
    for k, bS in enumerate(bruchSpalten):
        keineZahlBefore = keineZahl
        zahl, keineZahl, bsNeu = OrderedDict(), OrderedDict(), []
        for i, char in enumerate(bS):
            if char.isdecimal():
                """alles was Zahlen sind"""
                zahl[i] = char
            else:
                """alles was keine Zahlen sind"""
                keineZahl[i] = char
        flag: bool = False
        allVergleich: list[bool] = [
            zahl > c for c, zahl in zip(keineZahl.keys(), zahl.keys())
        ]
        """bool Liste wann es keine ist und wann eine zahl im string"""
        zahlSet: set = set(zahl.keys())
        keineZahlSet: set = set(keineZahl.keys())
        if len(zahlSet) == 0:
            return []
        anfang, ende = k == 0, k == len(bruchSpalten) - 1
        if anfang and all(allVergleich):
            flag = True
        elif ende and not any(allVergleich):
            flag = True
        elif (
            not anfang
            and not ende
            and keineZahlSet.issubset(range(min(zahlSet) + 1, max(zahlSet)))
        ):
            flag = True
        else:
            flag = False
        if flag is False:
            return []
        # bsAlt = bsNeu
        if len(keineZahlSet) > 0:
            zahlenGroesserSet, zahlenKleinerSet = grKl(zahlSet, keineZahlSet)
            """siehe erklärung der Fkt in Fkt"""
            zahlenKleinerDict: dict = getDictLimtedByKeyList(zahl, zahlenKleinerSet)
            zahlenGroesserDict: dict = getDictLimtedByKeyList(zahl, zahlenGroesserSet)
            """siehe erklärung der Fkt in Fkt"""
            if k == len(bruchSpalten) - 1 and len(zahlenGroesserDict) > 0:
                return []
            bsNeu = [zahlenKleinerDict, keineZahl, zahlenGroesserDict]
        elif k == 0 or k == len(bruchSpalten) - 1:
            bsNeu = [zahl]
        else:
            return []
        bruchSpaltenNeu += [bsNeu]
        if k == 1:
            vorZahl1 = (
                () if len(bruchSpaltenNeu[0]) == 1 else bruchSpaltenNeu[0][1].values()
            )
            vorZahl1 = tuple(vorZahl1)
            zahl1 = (
                bruchSpaltenNeu[0][0].values()
                if len(bruchSpaltenNeu[0]) == 1
                else bruchSpaltenNeu[0][2].values()
            )
            zahl2 = bruchSpaltenNeu[1][0].values()
            zahl1 = tuple(zahl1)
            zahl2 = tuple(zahl2)
            if k == len(bruchSpalten) - 1:
                nachZahl2 = (
                    ()
                    if len(bruchSpaltenNeu[-1]) == 1
                    else bruchSpaltenNeu[-1][1].values()
                )
                nachZahl2 = tuple(nachZahl2)
                bruchSpaltenNeu2 += [vorZahl1, zahl1 + zahl2, nachZahl2]
            else:
                bruchSpaltenNeu2 += [vorZahl1, zahl1 + zahl2]
        elif k == len(bruchSpalten) - 1 and k > 1:
            vorZahl1 = (
                () if len(bruchSpaltenNeu[-2]) == 1 else bruchSpaltenNeu[-2][1].values()
            )
            vorZahl1 = tuple(vorZahl1)
            zahl1 = (
                bruchSpaltenNeu[-2][0].values()
                if len(bruchSpaltenNeu[-2]) == 1
                else bruchSpaltenNeu[-2][2].values()
            )
            zahl2 = bruchSpaltenNeu[-1][0].values()
            zahl1 = tuple(zahl1)
            zahl2 = tuple(zahl2)
            nachZahl2 = (
                () if len(bruchSpaltenNeu[-1]) == 1 else bruchSpaltenNeu[-1][1].values()
            )
            nachZahl2 = tuple(nachZahl2)
            bruchSpaltenNeu2 += [vorZahl1, zahl1 + zahl2, nachZahl2]
        elif k > 1:
            vorZahl1 = (
                () if len(bruchSpaltenNeu[-2]) == 1 else bruchSpaltenNeu[-2][1].values()
            )
            vorZahl1 = tuple(vorZahl1)
            zahl1 = (
                bruchSpaltenNeu[-2][0].values()
                if len(bruchSpaltenNeu[-2]) == 1
                else bruchSpaltenNeu[-2][2].values()
            )
            zahl2 = bruchSpaltenNeu[-1][0].values()
            zahl1 = tuple(zahl1)
            zahl2 = tuple(zahl2)
            bruchSpaltenNeu2 += [vorZahl1, zahl1 + zahl2]
            # return bruchSpaltenNeu, bruchSpaltenNeu2
    return bruchSpaltenNeu2


def dictToList(dict_: dict) -> list:
    liste = []
    for key, value in dict_.items():
        liste += [value]
    return liste


# Ich muss eine Rangematrix machen

# def get2StrsFromBSlistList_old(bruchSpaltenListList: list) -> tuple[str, str]:
#    neuZahlVorBruchstrich = []
#    neuZahlNachBruchstrich = []
#    charsVorBruchStrich = []
#    charsNachBruchStrich = []
#    lastZahlVorBruchStrich = None
#    lastZahlNachBruchStrich = None
#    for i, bSLL in enumerate(bruchSpaltenListList):
#        zahl0List = dictToList(bSLL[0])
#        if len(bSLL) == 3:
#            chars1List = dictToList(bSLL[1])
#            zahl2List = dictToList(bSLL[2])
#
#            if tuple(bSLL[1].values()) == ("-",):
#                print("jaa")
#                zahlDavorVorBruchstrich = int("".join(lastZahlVorBruchStrich))
#                zahlDavorNachBruchstrich = int("".join(lastZahlNachBruchStrich))
#                zahlDanachVorBruchStrich = int("".join(zahl2List))
#                zahlDanachNachBruchStrich = int("".join(zahl0List))
#                zahlenDavor = range(
#                    zahlDavorVorBruchstrich, zahlDanachVorBruchStrich + 1
#                )
#                zahlenDanach = range(
#                    zahlDavorNachBruchstrich, zahlDanachNachBruchStrich
#                )
#                print(["zahlenDavor", zahlenDavor, "zahlenDanach", zahlenDanach])
#                neuZahlVorBruchstrich += chars1List + zahl2List
#                neuZahlNachBruchstrich += zahl0List + chars1List
#            else:
#                neuZahlVorBruchstrich += chars1List + zahl2List
#                neuZahlNachBruchstrich += zahl0List + chars1List
#            lastZahlVorBruchStrich = zahl2List
#            lastZahlNachBruchStrich = zahl0List
#        elif len(bSLL) == 1:
#            if i == 0:
#                neuZahlVorBruchstrich += zahl0List
#                lastZahlVorBruchStrich = zahl0List
#            elif i == len(bruchSpaltenListList) - 1:
#                neuZahlNachBruchstrich += zahl0List
#                lastZahlNachBruchStrich = zahl0List
#            else:
#                raise
#    return "".join(neuZahlVorBruchstrich), "".join(neuZahlNachBruchstrich)


def createRangesForBruchLists(bruchList: list) -> tuple:
    n1, n2 = [], []
    listenRange: range = range(0)
    flag = 0
    # ergebnis: list[tuple[range | str]] = []
    ergebnis = []
    for b in bruchList:
        if flag == -1:
            return []
        if flag > 3:
            """illegal"""
            return []
        elif flag == 3:
            """Es war ein Bruch"""
            ergebnis += [str(n2[-2]), "-", str(n2[-1])]
            listenRange = range(int(n1[-2]), int(n1[-1]) + 1)
            flag = -1
        if len(b) == 2 and (b[0] + b[1]).isdecimal():
            """Es ist ein Bruch"""
            n1 += [int(b[0])]
            n2 += [int(b[1])]
            flag += 1
        elif len(b) == 1 and b[0] == "-" and flag > 0:
            flag += 1
        else:
            """Es ist kein Bruch"""
            flag = 0
            ergebnis += [*b]
    ergebnis2 = "".join(ergebnis)
    return listenRange, ergebnis2


def alles(text) -> tuple:
    return createRangesForBruchLists(bruchSpalt(text))
