#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import sys
from collections import OrderedDict

sys.path.insert(0, "/home/alex/myRepos/reta")

import reta

heiler = list({(13 * n, 14 * n) for n in range(1, 9)})

heiler.sort()
print(heiler)
for i, (a, b) in enumerate(heiler):
    print("Paar: '{} mit {}'".format(a, b))
    reta.Program(
        [
            "reta",
            "-zeilen",
            "".join(
                (
                    "--vorhervonausschnitt=",
                    str(a),
                    ",",
                    str(b),
                )
            ),
            "-spalten",
            "--menschliches=motive",
            "-ausgabe",
            "--spaltenreihenfolgeundnurdiese=1",
            "--keineleereninhalte",
            "--art=bbcode",
            "--keineueberschriften" if i > 0 else "",
        ]
    )
    print()
    print()
