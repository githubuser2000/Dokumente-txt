#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

liste: list[int] = []
for a in range(5):
    for b in range(4):
        for c in range(3):
            liste += [5 + (3 ** a) * (5 ** b) * (11 ** c)]
liste.sort()
liste2: list[int] = []
for a in liste:
    if a < 122:
        liste2 += [a]
print(liste2)
