#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
# import numpy as np
import html
import json
import platform
import re
from collections import OrderedDict, namedtuple
from itertools import zip_longest
from typing import Optional, Union

try:
    from orderedset import OrderedSet
except:
    OrderedSet = set

from center import BereichToNumbers2, Primzahlkreuz_pro_contra_strs, retaHilfe
from tableHandling import (Enum, Iterable, Multiplikationen, OutputSyntax,
                           Tables, Union, alxp, bbCodeSyntax, cliout, copy,
                           csv, csvSyntax, deepcopy, emacsSyntax,
                           getTextWrapThings, htmlSyntax, infoLog,
                           markdownSyntax, math, os, output, primCreativity,
                           re, setShellRowsAmount, shellRowsAmount, sys, x)

gebrochenSpaltenMaximumPlus1 = 21


def render_color(tag_name, value, options, parent, context):
    return '<span style="color:%s;">%s</span>' % (tag_name, value)


class Program:
    def produceAllSpaltenNumbers(self, neg=""):
        global shellRowsAmount

        def resultingSpaltenFromTuple(
            tupl: tuple, neg, paraValue=None, befehlName=None
        ) -> tuple:
            for i, eineSpaltenArtmitSpaltenNummern in enumerate(tupl):
                """
                Die Variable self.tables.spalteGestirn braucht man gar nicht mehr !!!
                """
                if (
                    type(eineSpaltenArtmitSpaltenNummern) in [list, tuple]
                    and len(eineSpaltenArtmitSpaltenNummern) > 0
                ):
                    if type(eineSpaltenArtmitSpaltenNummern[0]) is bool:
                        eineSpaltenArtmitSpaltenNummern = set(
                            eineSpaltenArtmitSpaltenNummern
                        )
                    elif type(eineSpaltenArtmitSpaltenNummern[0]) in [tuple, list]:
                        eineSpaltenArtmitSpaltenNummern = set(
                            eineSpaltenArtmitSpaltenNummern[0]
                        )
                if i == 2 and (
                    type(eineSpaltenArtmitSpaltenNummern)
                    in [
                        list,
                        tuple,
                        # set,
                    ]
                    or befehlName in Program.ParametersMain.gebrochenuniversum[0]
                    or befehlName in Program.ParametersMain.gebrochengalaxie[0]
                ):
                    if befehlName == Program.ParametersMain.Multiplikationen[0]:
                        self.spaltenArtenKey_SpaltennummernValue[
                            (len(neg), 2)
                        ] |= Program.lambdaPrimGalax(paraValue)
                    elif befehlName in Program.ParametersMain.gebrochenuniversum[0]:
                        self.spaltenArtenKey_SpaltennummernValue[
                            (len(neg), 5)
                        ] |= Program.lambdaGebrUnivUndGalax(paraValue)
                    elif befehlName in Program.ParametersMain.gebrochengalaxie[0]:
                        self.spaltenArtenKey_SpaltennummernValue[
                            (len(neg), 6)
                        ] |= Program.lambdaGebrUnivUndGalax(paraValue)
                    else:
                        print(befehlName)
                        raise ValueError
                elif (
                    paraValue == "beschrieben"
                    and befehlName in Program.ParametersMain.primvielfache
                ):
                    self.spaltenArtenKey_SpaltennummernValue[(len(neg), 2)] |= {2}
                else:
                    try:
                        self.spaltenArtenKey_SpaltennummernValue[
                            (len(neg), i)
                        ] |= eineSpaltenArtmitSpaltenNummern
                    except TypeError:
                        pass
            return self.spaltenArtenKey_SpaltennummernValue

        def spalten_removeDoublesNthenRemoveOneFromAnother():
            for el2Type in range(
                int(len(self.spaltenArtenKey_SpaltennummernValue) / 2)
            ):
                self.spaltenArtenKey_SpaltennummernValue[(0, el2Type)] -= (
                    self.spaltenArtenKey_SpaltennummernValue[(0, el2Type)]
                    & self.spaltenArtenKey_SpaltennummernValue[(1, el2Type)]
                )
            for el2Type in range(
                int(len(self.spaltenArtenKey_SpaltennummernValue) / 2)
            ):
                self.spaltenArtenKey_SpaltennummernValue[
                    (0, el2Type)
                ] -= self.spaltenArtenKey_SpaltennummernValue.pop((1, el2Type))

        # def notNormalParameters(parameter, parametervalue, tables):
        #     if parameter == "bedeutung" and parametervalue in [
        #         "gestirn",
        #         "mond",
        #         "sonne",
        #         "planet",
        #     ]:
        #         tables.spalteGestirn = True

        # self.intoParameterDatatype
        self.mainParaCmds: dict = {
            "zeilen": 0,
            "spalten": 1,
            self.tables.getCombis.parameterName: 2,
            "ausgabe": 3,
            "debug": None,
            "h": None,
            "help": None,
        }
        # self.mainParaCmds2: dict = {
        #    0: "zeilen",
        #    1: "spalten",
        #    2: "kombination",
        #    3: "ausgabe",
        # }
        lastMainCmd: int = -1
        # kombiSpalten = OrderedSet()
        # ordinarySpalten = OrderedSet()

        # for cmd in self.argv[1:]:
        #    if (
        #        lastMainCmd == self.mainParaCmds["spalten"]
        #        or lastMainCmd == self.mainParaCmds["ausgabe"]
        #    ):
        #        self.breiteBreitenSysArgvPara(cmd, neg)
        for cmd in self.argv[1:]:
            if len(cmd) > 1 and cmd[0] == "-" and cmd[1] != "-":
                if cmd[1:] in self.mainParaCmds.keys():
                    lastMainCmd = self.mainParaCmds[cmd[1:]]
                elif cmd[1:] == "nichts":
                    pass
                elif len(neg) == 0:
                    # else:
                    cliout(
                        'Der Haupt-Parameter "'
                        + cmd
                        + '" existiert hier nicht als Befehl!'
                        + " Es ist nur möglich: -"
                        + str(", -".join(list(self.mainParaCmds.keys())))
                    )
            elif cmd[:2] == "--":
                if lastMainCmd == self.mainParaCmds["spalten"]:
                    cmd = cmd[2:]
                    eq = cmd.find("=")
                    if self.breiteBreitenSysArgvPara(cmd, neg):
                        pass
                    elif cmd == "keinenummerierung" and len(neg) == 0:
                        self.tables.nummeriere = False
                    elif eq != -1:
                        for oneOfThingsAfterEqSign in cmd[eq + 1 :].split(","):
                            if (
                                len(oneOfThingsAfterEqSign) > 0
                                and oneOfThingsAfterEqSign[0] == "-"
                            ):
                                oneOfThingsAfterEqSign = oneOfThingsAfterEqSign[1:]
                                yes1 = True if neg == "-" else False
                            else:
                                yes1 = True if len(neg) == 0 else False
                            if yes1:
                                try:
                                    resultingSpaltenFromTuple(
                                        self.paraDict[
                                            (cmd[:eq], oneOfThingsAfterEqSign)
                                        ],
                                        neg,
                                        oneOfThingsAfterEqSign,
                                        befehlName=cmd[:eq],
                                    )
                                except KeyError:
                                    nebenParameters: list = []
                                    nebenparameterWerte: list = []
                                    for value in self.paraDict.keys():
                                        nebenParameters += [value[0]]
                                        nebenparameterWerte += [value[1]]

                                    if cmd[:eq] in nebenParameters:
                                        possibleNebenparameterWert: list = []
                                        for nebenParameter, nebenparameterWert in zip(
                                            nebenParameters,
                                            nebenparameterWerte,
                                        ):
                                            if nebenParameter == cmd[:eq]:
                                                possibleNebenparameterWert += [
                                                    nebenparameterWert
                                                ]

                                        cliout(
                                            'Der Unter-Paramaeter "--'
                                            + cmd[:eq]
                                            + '" existiert, aber nicht mit dem Textwert "'
                                            + oneOfThingsAfterEqSign
                                            + (
                                                (
                                                    '". Mögliche Nebenparameter-Textwerte, für diesen Unter-Parameter, sind: "'
                                                )
                                                + (
                                                    ",".join(possibleNebenparameterWert)
                                                    + '"'
                                                )
                                                if (
                                                    len(possibleNebenparameterWert) > 0
                                                    and not all(
                                                        [
                                                            p == ""
                                                            for p in possibleNebenparameterWert
                                                        ]
                                                    )
                                                )
                                                else '". Stattdessen gibt keine Nebenparameter-Textwerte.'
                                            )
                                        )
                                    else:
                                        cliout(
                                            'Der Unter-Paramaeter "--'
                                            + cmd[:eq]
                                            + '" mit dem Textwert "'
                                            + oneOfThingsAfterEqSign
                                            + '" existiert hier nicht als Befehl für Haupt-Parameter'
                                            + " -spalten"
                                            + " !"
                                            + " Es ist nur möglich:\n--"
                                            + str(
                                                ", --".join(
                                                    tuple(
                                                        OrderedSet(
                                                            key[0]
                                                            for key in self.paraDict.keys()
                                                        )
                                                    )
                                                )
                                            )
                                            + ", --breiten, --breite"
                                            + "\nmit dem Werten dahinter:\n"
                                            + str(
                                                ",".join(
                                                    tuple(
                                                        OrderedSet(
                                                            key[1]
                                                            for key in self.paraDict.keys()
                                                        )
                                                    )
                                                )
                                            )
                                        )

                    else:
                        try:
                            if len(cmd) > 0 and (cmd[-1] == "-" and neg == "-") != (
                                len(neg) == 0 and cmd[-1] != "-"
                            ):
                                if len(cmd) > 0 and cmd[-1] == "-" and len(neg) > 0:
                                    cmd = cmd[:-1]

                                resultingSpaltenFromTuple(
                                    self.paraDict[(cmd, "")], neg, befehlName=cmd
                                )

                        except KeyError:
                            cliout(
                                'Der Unter-Parameter "--'
                                + cmd
                                + '" existiert hier nicht als Befehl für Haupt-Parameter'
                                + " -spalten"
                                + ", oder dieser Parameter braucht Werte analog wie: \n--unterParameter=Wert1\n"
                                + "Es ist nur möglich: --"
                                + str(
                                    ", --".join(
                                        tuple(
                                            OrderedSet(
                                                key[0] for key in self.paraDict.keys()
                                            )
                                        )
                                    )
                                )
                                + ", --keinenummerierung"
                            )

                elif (
                    lastMainCmd
                    == self.mainParaCmds[self.tables.getCombis.parameterName]
                ):
                    if cmd[:10] == "--galaxie=" or cmd[:12] == "--universum=":
                        for oneKombiSpalte in cmd[cmd.find("=") + 1 :].split(","):
                            if len(oneKombiSpalte) > 0 and oneKombiSpalte[0] == "-":
                                oneKombiSpalte = oneKombiSpalte[1:]
                                yes1 = True if neg == "-" else False
                            else:
                                yes1 = True if len(neg) == 0 else False
                            if yes1:
                                try:
                                    resultingSpaltenFromTuple(
                                        (
                                            OrderedSet(),
                                            OrderedSet(),
                                            OrderedSet(),
                                            {
                                                self.kombiReverseDict[oneKombiSpalte],
                                            }
                                            if cmd.find("=") == 9
                                            else OrderedSet(),
                                            OrderedSet(),
                                            OrderedSet(),
                                            OrderedSet(),
                                            OrderedSet(),
                                            {
                                                self.kombiReverseDict2[oneKombiSpalte],
                                            }
                                            if cmd.find("=") == 11
                                            else OrderedSet(),
                                        ),
                                        neg,
                                        befehlName="kombinationen",
                                    )
                                except KeyError:
                                    cliout(
                                        'Die Kombispalte "'
                                        + oneKombiSpalte
                                        + '" existiert so nicht als Befehl. Möglich sind die Parameter für '
                                        + cmd[: cmd.find("=") + 1]
                                        + " "
                                        + (
                                            str(self.kombiReverseDict.keys())[11:-1]
                                            if cmd[: cmd.find("=")] == "--galaxie"
                                            else str(self.kombiReverseDict2.keys())[
                                                11:-1
                                            ]
                                            if cmd[: cmd.find("=")] == "--universum"
                                            else ""
                                        )
                                    )

                    else:
                        cliout(
                            'kein Unter-Parameter "--galaxie=" oder "--universum=" angegeben für Hauptparameter -kombination'
                        )
                elif lastMainCmd not in self.mainParaCmds.values():
                    cliout(
                        "Es muss ein Hauptparameter, bzw. der richtige, gesetzt sein, damit ein"
                        + ' Nebenparameter, wie möglicherweise: "'
                        + cmd
                        + '" ausgeführt werden kann. Hauptparameter sind: -'
                        + " -".join(self.mainParaCmds)
                    )
        if "--breite=0" in self.argv:
            self.breiteBreitenSysArgvPara("--breite=0", "")
        if len(neg) == 0:
            self.produceAllSpaltenNumbers("-")
            spalten_removeDoublesNthenRemoveOneFromAnother()

    def breiteBreitenSysArgvPara(self, cmd, neg) -> bool:
        global shellRowsAmount
        # alxp(
        #    "shellRowsAmount war in reta.py wegen dem Setzen der Breite auf {} gesetzt".format(
        #        shellRowsAmount
        #    )
        # )

        if cmd[:7] == "breite=":
            shellRowsAmount, _, _, _ = getTextWrapThings()
            if self.breiteHasBeenOnceZero:
                shellRowsAmount = 0
                self.tables.textWidth = 0
                self.breiteORbreiten = True
                return True
            if cmd[7:].isdecimal():
                breite = abs(int(cmd[7:]))
                if breite == 0:
                    self.breiteHasBeenOnceZero = True
                    shellRowsAmount = 0
                elif shellRowsAmount > 7 and breite > shellRowsAmount - 7:
                    breite = shellRowsAmount - 7
                # alxp(
                #    "X1 textW von {} in {} ändern".format(self.tables.textWidth, breite)
                # )
                try:
                    self.tables.textWidth = (
                        breite
                        if breite > self.tables.textWidth
                        else self.tables.textWidth
                    )
                except:
                    self.tables.textWidth = breite
                self.breiteORbreiten = True
            return True
        elif cmd[:8] == "breiten=" and len(neg) == 0:
            self.tables.breitenn = []
            for breite in cmd[8:].split(","):
                if breite.isdecimal():
                    self.tables.breitenn += [int(breite)]
                    self.breiteORbreiten = True
            return True
        return False

    def storeParamtersForColumns(self):
        # global puniverseprims
        def intoParameterDatatype(
            parameterMainNames: tuple, parameterNames: tuple, datas: tuple
        ) -> tuple:
            """
            ALLE PARAMETER DIESER FUNKTION SIND EIGENTLICH NUR EIN JEWEILIGES ELEMENT VON
            paraNdataMatrix
            ZUSAMMEN

            Speichert einen Parameter mit seinem DatenSet
            in 2 Datenstrukturen (die beides kombinieren 2x2)
            Diese werden jedoch nur zurück gegeben und nicht in der Klasse gespeichert.
            @return: alle Hauptparamter| alle Nebenparamter zu nur einem
            Hauptparameter ergibt Mengen an Spalten | enthält alle Haup- und
            Nebenparameter keys sind Spalten der Tabelle
            """
            paraMainDict = {}
            for name in parameterMainNames:
                paraMainDict[name] = parameterNames
            paraDict = {}
            for name1 in parameterMainNames:
                for name2 in parameterNames:
                    paraDict[(name1, name2)] = datas
                if len(parameterNames) == 0:
                    paraDict[(name1, "")] = datas
            dataDicts: tuple = ({}, {}, {}, {}, {}, {}, {}, {}, {})

            # datas sind nicht die Haupt-und-Neben-Parameter, sondern alles das diese enthalten und meinen können
            # ein datas Datensatz sind alle sets, die ein Haupt-Neben-Parameter Zusammenhang enthalten kann an sets
            for i, d in enumerate(datas):
                for spaltenNummerOderEtc in d:
                    # spaltenNummerOderEtc ist hier also eine Zahl von einem set, die z.B. eine Spaltennummer meinen kann
                    into = []
                    parameterMainNamePerLoop = []
                    case: int = None

                    # das mit 2 Schleifen nur deshalb, damit immer alle Haupt- und Neben-Parameter in die Liste rein kommen
                    for parameterMainName in parameterMainNames:
                        for parameterName in (
                            parameterNames if len(parameterNames) > 0 else ("",)
                        ):
                            # i ist die Nummer welches Set es ist
                            if i == 4 and (
                                type(spaltenNummerOderEtc) is bool
                                or (
                                    type(spaltenNummerOderEtc) in [tuple, list]
                                    and len(spaltenNummerOderEtc) > 0
                                    and type(spaltenNummerOderEtc[0]) is bool
                                )
                            ):
                                case = 1
                                into += [
                                    (
                                        parameterMainName,
                                        parameterName,
                                    )
                                ]
                            elif i in (5, 6):  # and type(spaltenNummerOderEtc) is set:
                                case = 2
                                into += [[(parameterMainName, parameterName)]]
                                parameterMainNamePerLoop += [parameterName]
                            elif i == 2 and callable(spaltenNummerOderEtc):
                                case = 2
                                parameterMainNamePerLoop += [parameterName]
                                into += [[(parameterMainName, parameterName)]]
                            elif i == 4 and (
                                type(spaltenNummerOderEtc) in (list, tuple)
                            ):
                                case = 4
                                into += [(parameterMainName, parameterName)]
                            elif i == 4 and (type(spaltenNummerOderEtc) in (set,)):
                                case = 4
                                into += [(parameterMainName, parameterName)]
                                spaltenNummerOderEtc = spaltenNummerOderEtc.pop()
                            else:
                                case = 3
                                try:
                                    into += [(parameterMainName, parameterName)]
                                except KeyError:
                                    into = [(parameterMainName, parameterName)]

                    index1 = i if case != 1 else 3
                    index2a = (
                        spaltenNummerOderEtc
                        if case == 3
                        else (
                            spaltenNummerOderEtc
                            if case == 4
                            else ("bool", 0)
                            if case == 1
                            else tuple(
                                (
                                    int(para)
                                    if para.isdecimal()
                                    else para
                                    if len(parameterNames) > 0
                                    else None
                                    for para in parameterMainNamePerLoop
                                )
                            )
                            if case == 2
                            else None
                        )
                    )
                    intoA = into if case == 2 else (into,)
                    for index2, into2 in zip_longest(
                        index2a if case == 2 else (index2a,), intoA, fillvalue=into
                    ):
                        try:
                            dataDicts[index1][index2] += (
                                (into2,)
                                if dataDicts[index1][index2][-1] != into2
                                else ()
                            )
                        except KeyError:
                            dataDicts[index1][index2] = (into2,)
            return paraMainDict, paraDict, dataDicts

        def mergeParameterDicts(
            paraMainDict1: dict,
            paraDict1: dict,
            dataDicts1: list,
            paraMainDict2: dict,
            paraDict2: dict,
            dataDicts2: list,
        ) -> tuple:
            """Merged die beiden 2x2 Datenstrukturen und speichert diese
            in die Klasse und gibt sie dennoch auch mit return zurück
            @param paraMainDict: Hauptparameter in der Kommandozeile
            hat als Werte die Nebenparameter und keys sind die Hauptparamter
            @param paraDict: Nebenparamteter in der Kommandozeile
            hat als Werte die Spaltennummern dazugehörig
            @param dataDicts: die beiden Parameter sagen welche Spaltennummern es
            sein werden
            @return: Spaltennummer sagt welche Parameter es ingesamt dazu sind | die
            beiden Parameter sagen, welche Spalten es alle sind.

            *paraNdataMatrix*
            enthält die meisten Parameternamen mit den zugehörigen Spaltennummern mit Sonderdaten, weil einige Spalten generiert werden aus anderen

            u.a. daraus wird das *paraDict* und *dataDict* gebaut. Beides hat das Gleiche drin, nur das andere jeweils mit Key und Value vertauscht.
            Darin sind die Paramenternamen und csv Spaltennummern drin, die nicht verwechselt werden dürfen mit den dann real vorhandenen Spaltennummern, die nicht die gleichen als Zahl sind, wie die in der CSV-Datei.

            *self.tables.generatedSpaltenParameter*
            key ist Spaltennummer der Ausgabe, value ist ein Paar von 2 Strings über Überparametername und Unterparametername für den Klassenname für die Spalte des HTML-Tags.
            <em>
            Das beinhaltet das für alle Parameter und Ausgabe-Spalten-Nummern.</em>"""
            global gebrochenSpaltenMaximumPlus1

            paraMainDict1 = {**paraMainDict1, **paraMainDict2}
            paraDict1 = {**paraDict1, **paraDict2}
            dataDicts3 = deepcopy(dataDicts1)
            for i, (dict1, dict2) in enumerate(zip_longest(dataDicts1, dataDicts2)):
                if type(dict1) is dict and type(dict2) is dict:
                    if len(dataDicts3[i].keys()) == 0:
                        dataDicts3[i] = dataDicts2[i]
                    else:
                        for key1, value1 in dict1.items():
                            for key2, value2 in dict2.items():
                                if key2 == key1:
                                    dataDicts3[i][key1] += value2
                                elif key2 not in dataDicts3[i].keys():
                                    dataDicts3[i][key2] = value2
                elif type(dict1) is dict and dict2 is None:
                    dataDicts3[i] = dict1
                elif dict1 is None and type(dict2) is dict:
                    dataDicts3[i] = dict2
            return paraDict1, dataDicts3

        Program.ParametersMain: namedtuple[str, str] = namedtuple(
            "ParametersMain",
            "wichtigste wichtigste2 religionen galaxie strukturgroesse universum wirtschaft menschliches procontra licht bedeutung symbole Multiplikationen konzept konzept2 inkrementieren operationen universummetakonkret primzahlwirkung gebrochenuniversum gebrochengalaxie primvielfache planet strukturenkleinere grundstrukturen alles",
        )

        Program.ParametersMain: namedtuple[tuple[str]] = Program.ParametersMain(
            ("Wichtigstes_zum_verstehen", "wichtigsteverstehen"),
            ("Wichtigstes_zum_gedanklich_einordnen", "wichtigsteeinordnen"),
            (
                "Religionen",
                "religionen",
                "religion",
            ),
            (
                "Galaxie",
                "galaxie",
                "alteschriften",
                "kreis",
                "galaxien",
                "kreise",
            ),
            (
                "Größenordnung",
                "groessenordnung",
                "strukturgroesse",
                "strukturgroeße",
                "strukturgrösse",
                "strukturgröße",
                "groesse",
                "stufe",
                "organisationen",
            ),
            (
                "Universum",
                "universum",
                "transzendentalien",
                "strukturalien",
                "kugel",
                "kugeln",
                "ball",
                "baelle",
                "bälle",
            ),
            ("Wirtschaft", "wirtschaft"),
            (
                "Menschliches",
                "menschliches",
            ),
            (
                "Pro_Contra",
                "procontra",
                "dagegendafuer",
            ),
            (
                "Licht",
                "licht",
            ),
            (
                "Bedeutung",
                "bedeutung",
            ),
            (
                "Symbole",
                "symbole",
            ),
            tuple(a[0] for a in Multiplikationen),
            (
                "Eigenschaften_n",
                "eigenschaften",
                "eigenschaft",
                "konzept",
                "konzepte",
            ),
            ("Eigenschaften_1/n", "konzept2", "konzepte2"),
            (
                "Inkrementieren",
                "inkrementieren",
            ),
            (
                "Operationen",
                "operationen",
            ),
            (
                "Meta_vs_Konkret_(Universum)",
                "universummetakonkret",
            ),
            (
                "Primzahlwirkung",
                "primzahlwirkung",
            ),
            ("gebrochenuniversum",),
            ("gebrochengalaxie",),
            ("Multiplikationen", "multiplikationen"),
            ("Planet_(10_und_oder_12)", "planet"),
            ("Strukturen_1_bis_9", "strukturkleinerzehn"),
            ("Grundstrukturen", "grundstrukturen"),
            ("alles",),
        )

        allowedPrimNumbersForCommand: tuple[str] = tuple(
            (
                str(num)
                for num in tuple(
                    OrderedSet(
                        (
                            num if primCreativity(num) == 1 else None
                            for num in range(2, 32)
                        )
                    )
                    - {None}
                )
            )
        )

        Program.lambdaGebrUnivUndGalax = lambda paraValues: {
            abs(int(chosen)) if chosen.isdecimal() else None
            for chosen in [value for value in (paraValues.split(","))]
        } - {None, 0, 1}

        Program.lambdaPrimGalax = lambda paraValues: {
            abs(int(chosen))
            if chosen.isdecimal() and primCreativity(abs(int(chosen))) == 1
            else None
            for chosen in [value for value in (paraValues.split(","))]
        } - {None, 0, 1}

        paraNdataMatrix: list[
            tuple[
                tuple[str],
                set[int],
                set[tuple[int]],
                set,
                set,
                set[tuple[Optional[int], Optional[int]]],
                set,
                set[list[str]],
                set[str],
            ]
        ] = [
            (
                Program.ParametersMain.wichtigste,
                (
                    "Wichtigste",
                    "wichtigste",
                ),
                {10, 5, 4, 8},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Mensch-zu-Tier", "menschtier", "tiermensch"),
                {314},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Ansichten_Standpunkte_(18_17)", "ansichten"),
                {240, 346},
            ),
            (
                Program.ParametersMain.menschliches,
                ("(politische)_Richtungen_(7)", "richtungen", "politische"),
                {235},
            ),
            (
                Program.ParametersMain.planet,
                ("Wirklichkeiten_(10)", "wirklichkeit", "wirklichkeiten"),
                {233, 265, 268, 322},
            ),
            (
                Program.ParametersMain.planet,
                (
                    "Meta-Systeme_(12)",
                    "metasysteme",
                    "metasystem",
                    "meta-systeme",
                    "meta-system",
                ),
                {232, 288, 334},
            ),
            (
                Program.ParametersMain.planet,
                ("Intelligenz", "intelligenz"),
                {214},
            ),
            (
                Program.ParametersMain.planet,
                ("Gleichheit_Freiheit_Ordnung", "gleichheit", "freiheit", "ordnung"),
                {132, 324, 328, 79, 80, 331, 335},
            ),
            (
                Program.ParametersMain.planet,
                ("Komplexität", "komplexität", "komplexitaet"),
                {213},
            ),
            (
                Program.ParametersMain.planet,
                ("Mechanismen", "mechanismen", "mechanismus"),
                {107},
            ),
            (
                Program.ParametersMain.wichtigste,
                (
                    "Zweitwichtigste",
                    "zweitwichtigste",
                ),
                {19, 65, 183},
                set(),
                set(),
                set(),
                {(10,)},
            ),
            (
                Program.ParametersMain.wichtigste,
                (
                    "Drittwichtigste",
                    "drittwichtigste",
                ),
                {64},
            ),
            (
                Program.ParametersMain.wichtigste,
                ("Motive_Sternpolygone", "viertwichtigste"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primMotivStern"},
            ),
            (
                Program.ParametersMain.wichtigste2,
                ("Wichtigste", "wichtigstes"),
                {0, 1, 2, 36, 37, 207},
            ),
            (
                Program.ParametersMain.wichtigste2,
                ("Zweitwichtigste", "zweitwichtigste"),
                {30},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "Halbierung",
                    "halbierung",
                    "halbierungen",
                ),
                {86},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "Religions-Gründer-Typ",
                    "religionsgründertyp",
                    "prophet",
                    "archon",
                    "religionsgruendertyp",
                ),
                {72},
            ),
            (
                Program.ParametersMain.religionen,
                ("Hinduismus", "hinduismus"),
                {217},
            ),
            (
                Program.ParametersMain.religionen,
                ("Sternpolygon", "sternpolygon"),
                {0, 6, 36},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "der_Tierkreiszeichen",
                    "dertierkreiszeichen",
                    "babylon",
                ),
                {0, 36, 207},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "Sternpolygon_vs_gleichförmiges",
                    "vergleich",
                    "sternpolygonvsgleichfoermiges",
                    "vergleichnvs1divn",
                ),
                {87},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "Messias",
                    "messias",
                    "heptagramm",
                    "hund",
                    "messiase",
                    "messiasse",
                ),
                {7},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "gleichförmiges_Polygon",
                    "gleichförmigespolygon",
                    "gleichfoermigespolygon",
                    "nichtsternpolygon",
                    "polygon",
                ),
                {16, 37},
            ),
            (
                Program.ParametersMain.religionen,
                (
                    "Vertreter_höherer_Konzepte",
                    "vertreterhoehererkonzepte",
                    "galaxien",
                    "galaxie",
                    "schwarzesonne",
                    "schwarzesonnen",
                    "universum",
                    "universen",
                    "kreis",
                    "kreise",
                    "kugel",
                    "kugeln",
                ),
                {23},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "Offenbarung_des_Johannes",
                    "offenbarung",
                    "offenbarungdesjohannes",
                    "johannes",
                    "bibel",
                    "offenbarungjohannes",
                ),
                {90},
            ),
            (
                Program.ParametersMain.inkrementieren,
                ("Teilchen-Meta-Physik", "addition", "identitaet", "Identität"),
                {219, 223, 307, 308, 333},
            ),
            (
                Program.ParametersMain.galaxie,
                ("Hochzüchten", "hochzüchten", "hochzuechten"),
                {318, 319},
            ),
            (
                Program.ParametersMain.universum,
                ("Universelles_Verhältnis_gleicher_Zahlen", "verhaeltnisgleicherzahl"),
                {383},
            ),
            (
                Program.ParametersMain.universum,
                ("universelles_Recht", "recht", "jura"),
                {382, 34, 65},
            ),
            (
                Program.ParametersMain.universum,
                ("sowas_wie_Kombinieren_Verknüpfen", "kombinierenetc"),
                {320},
            ),
            (
                Program.ParametersMain.universum,
                ("Hochzüchten", "hochzüchten", "hochzuechten"),
                {318, 319},
            ),
            (
                Program.ParametersMain.universum,
                ("Teilchen-Meta-Physik", "addition", "identitaet", "Identität"),
                {219, 223, 307, 308, 333},
            ),
            (
                Program.ParametersMain.universum,
                ("keine_Nur-Paradigma-Religionen", "metaparadigmareligion"),
                {190, 191, 196},
            ),
            (
                Program.ParametersMain.universum,
                ("Kugeln_Kreise", "kugelnkreise", "kugeln", "kreise"),
                {77, 145},
            ),
            (
                Program.ParametersMain.galaxie,
                ("Kugeln_Kreise", "kugelnkreise", "kugeln", "kreise"),
                {77, 145},
            ),
            (
                Program.ParametersMain.galaxie,
                ("chinesisches_Horoskop", "chinesischeshoroskop", "china"),
                {91},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "babylonische_Tierkreiszeichen",
                    "tierkreiszeichen",
                    "babylon",
                ),
                {1, 2},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "Thomasevangelium",
                    "thomasevangelium",
                    "thomas",
                ),
                {0, 3, 303},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "analytische_Ontologie",
                    "analytischeontologie",
                    "ontologie",
                ),
                {84},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "Transzendentalien_innen_außen",
                    "innenaussenstrukur",
                    "strukturalieninnenaußen",
                    "strukturalieninnenaussen",
                    "innenaußenstrukur",
                    "transzendentalieninnenaußen",
                    "transzendentalieninnenaussen",
                ),
                {149},
            ),
            (
                Program.ParametersMain.galaxie,
                (
                    "Modallogik",
                    "modallogik",
                ),
                {148},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "5",
                    "fünf",
                    "fünfer",
                    "fünferstruktur",
                    "fuenf",
                    "fuenfer",
                    "fuenferstruktur",
                ),
                {96},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "9",
                    "neun",
                    "neuner",
                    "neunerstruktur",
                ),
                {94},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "3",
                    "drei",
                    "dreier",
                    "dreierstruktur",
                ),
                {92, 93, 315, 316},
            ),
            (
                Program.ParametersMain.strukturgroesse,
                (
                    "Licht",
                    "licht",
                ),
                {20, 27, 313},
            ),
            (
                Program.ParametersMain.strukturgroesse,
                (
                    "Strukturgrösse",
                    "größe",
                    "groesse",
                    "gross",
                    "strukturgroesse",
                    "strukturgroeße",
                    "strukturgrösse",
                    "strukturgröße",
                ),
                {4, 21, 54, 197},
            ),
            (
                Program.ParametersMain.strukturgroesse,
                ("Organisationen", "organisationen", "organisation"),
                {30, 82},
            ),
            (
                Program.ParametersMain.strukturgroesse,
                ("politische_Systeme", "politischesysteme", "politik"),
                {83},
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("meta",),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        2,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("konkret",),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        2,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("Theorie", "theorie"),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        3,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("Praxis", "praxis"),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        3,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "Management",
                    "management",
                    "stau",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        4,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "verändernd",
                    "veraendernd",
                    "fluss",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        4,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("ganzheitlich", "mathematisch_diskret", "diskret"),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        5,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "darüber_hinausgehend",
                    "hinausgehend",
                    "kontinuierlich",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        5,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Universum_Strukturalien_Transzendentalien",
                    "universum",
                    "strukturalie",
                    "strukturalien",
                    "transzendentalien",
                    "transzendentalie",
                ),
                set(),
                set(),
                set(),
                set(),
                {(5,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Richtung_als_Richtung",
                    "richtungrichtung",
                ),
                set(),
                set(),
                set(),
                set(),
                {(None,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Galaxieabsicht",
                    "absichtgalaxie",
                    "absicht",
                    "motive",
                    "motiv",
                    "absichten",
                    "galaxie",
                ),
                set(),
                set(),
                set(),
                set(),
                {(10,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Absicht_Reziproke_Galaxie",
                    "absichtgalaxiereziproke",
                    "absichtreziproke",
                    "motivereziproke",
                    "motivreziproke",
                    "absichtenreziproke",
                    "galaxiereziproke",
                ),
                set(),
                set(),
                set(),
                set(),
                {(42,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Universum_Reziproke",
                    "universumreziproke",
                    "strukturaliereziproke",
                    "strukturalienreziproke",
                    "transzendentalienreziproke",
                    "transzendentaliereziproke",
                ),
                set(),
                set(),
                set(),
                set(),
                {(131,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "Dagegen-Gegentranszendentalie",
                    "dagegengegentranszendentalie",
                    "dagegengegentranszendentalien",
                    "dagegengegenstrukturalien",
                    "dagegengegenstrukturalie",
                ),
                set(),
                set(),
                set(),
                set(),
                {(138,)},
            ),
            (
                Program.ParametersMain.primzahlwirkung,
                (
                    "neutrale_Gegentranszendentalie",
                    "neutralegegentranszendentalie",
                    "neutralegegentranszendentalien",
                    "neutralegegenstrukturalien",
                    "neutralegegenstrukturalie",
                ),
                set(),
                set(),
                set(),
                set(),
                {(202,)},
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "Unternehmung_Geschäft",
                    "unternehmen",
                    "unternehmung",
                    "geschaeft",
                    "geschäft",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        6,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                ("wertvoll", "wert"),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        6,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "Beherrschen",
                    "regieren",
                    "beherrschen",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        7,
                        0,
                    )
                },
            ),
            (
                Program.ParametersMain.universummetakonkret,
                (
                    "Richtung",
                    "richtung",
                    "gut",
                ),
                set(),
                set(),
                set(),
                set(),
                {
                    (
                        7,
                        1,
                    )
                },
            ),
            (
                Program.ParametersMain.universum,
                (
                    "analytische_Ontologie",
                    "analytischeontologie",
                    "ontologie",
                ),
                {84},
            ),
            (
                Program.ParametersMain.universum,
                (
                    "Gegentranszendentalien",
                    "gegentranszendentalien",
                    "gegentranszendentalie",
                    "gegenstrukturalien",
                    "gegenalien",
                    "gegenuniversalien",
                ),
                {138, 202},
            ),
            (
                Program.ParametersMain.universum,
                ("Systemsachen", "systemsachen"),
                {
                    150,
                },
            ),
            (
                Program.ParametersMain.universum,
                (
                    "Transzendentalien",
                    "transzendentalien",
                    "transzendentalie",
                    "strukturalien",
                    "alien",
                    "universalien",
                ),
                {5, 54, 55, 198},
            ),
            (
                Program.ParametersMain.universum,
                (
                    "Reziproke_von_Transzendentalien",
                    "transzendentalienreziproke",
                    "transzendentaliereziproke",
                    "strukturalienreziproke",
                    "alienreziproke",
                    "universalienreziproke",
                ),
                {131, 201},
            ),
            (
                Program.ParametersMain.universum,
                ("Netzwerk", "netzwerk"),
                {25},
            ),
            (
                Program.ParametersMain.universum,
                (
                    "warum_Transzendentalie_=_Strukturgroesse_=_Charakter",
                    "warumtranszendentaliezustrukturgroesseundcharakter",
                ),
                {4, 54, 5, 165},
            ),
            (
                Program.ParametersMain.universum,
                ("Kategorie", "kategorie"),
                {204, 205, 281},
            ),
            (Program.ParametersMain.universum, ("Raum-Missionen", "weltall"), {218}),
            (
                Program.ParametersMain.universum,
                ("Programmier-Paradigmen", "programmierparadigmen"),
                {351},
            ),
            (Program.ParametersMain.galaxie, ("Raum-Missionen", "weltall"), {218}),
            (
                Program.ParametersMain.universum,
                ("Geist__(15)", "geist"),
                {242},
            ),
            (
                Program.ParametersMain.universum,
                (
                    "warum_Transzendentalie_=_Komplexität_von_Michael_Commons",
                    "warumtranszendentaliegleichkomplexitaet",
                ),
                {65, 5, 166},
            ),
            (
                Program.ParametersMain.universum,
                (
                    "Model_of_Hierarchical_Complexity",
                    "modelofhierarchicalcomplexity",
                    "komplex",
                    "komplexität",
                    "komplexitaet",
                    "complexity",
                    "model",
                    "abstraktion",
                ),
                {65, 75, 203},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "2",
                    "zwei",
                    "gerade",
                    "ungerade",
                    "alternierung",
                    "alternierend",
                    "zweierstruktur",
                ),
                {78, 79, 80, 331},
            ),
            (
                Program.ParametersMain.operationen,
                (
                    "Multiplikation",
                    "multiplikation",
                ),
                {158},
            ),
            (
                Program.ParametersMain.operationen,
                ("4", "vier", "viererstruktur", "viererabfolgen"),
                {76, 77, 81, 104, 145},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Gesellschaftsschicht", "klasse", "klassen"),
                {241},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Moral", "moral", "warummoral"),
                {215, 216},
                {(216, 221)},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Fachgebiete", "fachgebiete", "fachbereiche", "themen"),
                {183},
            ),
            (
                Program.ParametersMain.wirtschaft,
                ("Fachgebiete", "fachgebiete", "fachbereiche", "themen"),
                {183},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "Pflanzen",
                    "pflanzen",
                ),
                {113},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "Maschinen",
                    "maschinen",
                    "maschine",
                    "gerät",
                    "geräte",
                    "geraete",
                    "geraet",
                ),
                {89},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "Organisationsform",
                    "organisationsform",
                    "organisationsart",
                    "firma",
                    "verein",
                ),
                {99},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "System",
                    "system",
                ),
                {
                    69,
                },
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "realistisch",
                    "funktioniert",
                ),
                {70},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "Erklärung",
                    "erklärung",
                    "erklaerung",
                ),
                {71},
            ),
            (
                Program.ParametersMain.wirtschaft,
                (
                    "BWL",
                    "bwl",
                ),
                {109},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Sinn_des_Lebens",
                    "sinndeslebens",
                    "lebenssinn",
                    "sinn",
                    "sinnsuche",
                ),
                {88, 189},
                {(181, 182)},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Intelligenzprobleme",
                    "intelligenzprobleme",
                    "intelligenzmaengel",
                    "intelligenzmängel",
                ),
                {147},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Denkweise_von_Lebewesen", "lebewesendenkweise", "denkweise"),
                {146},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Gegentranszendentalien",
                    "gegentranszendentalien",
                    "gegenstrukturalien",
                ),
                {138, 139, 202},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Gleichheit_Freiheit",
                    "gleichheitfreiheit",
                    "ungleichheit",
                    "dominieren",
                    "gleichheit",
                    "freiheit",
                ),
                {132, 328, 331, 335},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Gefühle",
                    "emotionen",
                    "gefuehle",
                    "gefuehle",
                    "emotion",
                    "gefühl",
                    "gefuehl",
                ),
                {105, 230, 243, 283, 284, 285, 286, 305},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Egoismus", "egoismus", "altruismus", "selbstlosigkeit"),
                {136},
                {(66, 67)},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Wirkung",
                    "wirkung",
                ),
                {135},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "INCELs",
                    "incel",
                    "incels",
                ),
                {68},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "irrationale_Zahlen_durch_Wurzelbildung",
                    "irrationalezahlendurchwurzelbildung",
                    "ausgangslage",
                ),
                {73},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "dominierendes_Geschlecht",
                    "dominierendesgeschlecht",
                    "maennlich",
                    "männlich",
                    "weiblich",
                ),
                {51},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Liebe",
                    "liebe",
                    "ethik",
                ),
                {8, 9, 28, 208, 330},
                {(121, 122)},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Glaube_Erkenntnis",
                    "glauben",
                    "erkenntnis",
                    "glaube",
                ),
                {59},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Angreifbarkeit",
                    "angreifbarkeit",
                    "angreifbar",
                ),
                {58, 57},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Strukturalien_bzw_Meta-Paradigmen_bzw_Transzendentalien_(15)",
                    "Transzendentalien",
                    "transzendentalien",
                    "transzendentalie",
                    "strukturalien",
                    "alien",
                    "universalien",
                    "meta-paradigmen",
                ),
                {5, 229, 131},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Bedingung_und_Auslöser_(1/3)",
                    "bedingung",
                    "bedingungen",
                    "auslöser",
                    "ausloeser",
                ),
                {338},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Relation_zueinander_reziprok_Universellen_(18→n_vs._1/n)",
                    "relativreziprokuniversell",
                ),
                {350},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("universeller_Komperativ_(18→15)", "universellerkomperativ"),
                {349},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Existenzialien_(3)", "existenzialien"),
                {348},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Extremalien_(19)", "extremalien"),
                {347, 352},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Erwartungshaltungen_(26)", "erwartungen", "erwartungshaltungen"),
                {344},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Leidenschaften_(21)", "leidenschaft", "leidenschaften"),
                {343},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("relativer_Zeit-Betrag_(15_10_4_18_6)", "relativerzeitbetrag"),
                {339},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Zahlenvergleich_(15_18_6)", "zahlenvergleich"),
                {340},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Bestrebungen(1/5)", "bestrebung", "bestrebungen"),
                {332},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Prinzipien(1/8)", "prinzipien"),
                {329, 378},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Attraktionen_(36)", "attraktionen"),
                {311},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Optimierung_(10)",
                    "optimierung",
                ),
                {310},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Themen_(6)",
                    "themen",
                    "thema",
                ),
                {309},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Bedeutung_(10)",
                    "bedeutung",
                ),
                {306},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Reziprokes",
                    "reziproke",
                    "reziprokes",
                ),
                {
                    42,
                    131,
                    204,
                    231,
                    273,
                    257,
                    284,
                    285,
                    257,
                    204,
                    205,
                    281,
                    326,
                    327,
                    328,
                    329,
                    330,
                    331,
                    332,
                    334,
                    335,
                    338,
                },
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Achtung_(4)", "achtung", "achten"),
                {270},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Zeit_(4)_als_Wirklichkeit", "zeit"),
                {266, 267},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_16_ist_zu_genügen", "absicht16"),
                {312},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_17_ist_zu_meinen", "absicht17"),
                {263},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_6_ist_Vorteilsmaximierung", "absicht6"),
                {262},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_7_ist_Selbstlosigkeit", "absicht7"),
                {261},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Regungen_(1)", "regung", "regungen"),
                {282},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Verhalten_(11)", "verhalten"),
                {301, 302},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Energie_und_universelle_Eigenschaften_(30)",
                    "energie",
                    "universelleeigenschaften",
                    "lebensenergie",
                ),
                {287, 293},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Garben_und_Verhalten_nachfühlen(31)",
                    "garben",
                    "verhaltenfuehlen",
                    "verhaltenfühlen",
                ),
                {295},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    Primzahlkreuz_pro_contra_strs[1],
                    "nachvollziehen",
                ),
                {242, 297},
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primzahlkreuzprocontra"},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Empathie_(37)", "empathie", "mitgefuehl"),
                {294},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Absicht_1/6_ist_Reinigung_und_Klarheit",
                    "absicht1/6",
                    "absicht1pro6",
                ),
                {298},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_10_ist_Wirklichkeit_erkennen", "absicht10"),
                {260},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Geist_(15)",
                    "geist",
                    "bewusstsein",
                ),
                {229, 231, 242, 273, 297, 304},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Reflexe_(3)",
                    "reflex",
                    "reflexe",
                ),
                {256},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Lust_(9)",
                    "lust",
                ),
                {255},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Paradigmen_sind_Absichten_(13)",
                    "paradigmen",
                    "absichten",
                ),
                {10, 42},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Wirklichkeiten_Wahrheit_Wahrnehmung_(10)",
                    "wirklichkeit",
                    "wirklichkeiten",
                    "wahrheit",
                    "wahrnehmung",
                ),
                {233, 265, 268, 322, 342},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Stimmungen_Kombinationen_(14)",
                    "stimmung",
                    "stimmungen",
                    "kombination",
                    "kombinationen",
                ),
                {290, 296, 325, 326, 327},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Klassen_(20)", "klasse", "klassen"),
                {241, 289},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Ordnung_und_Filterung_12_und_1pro12",
                    "ordnen",
                    "ordnenundfiltern",
                    "filtern",
                ),
                {132, 328, 331, 335},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Meta-Systeme_(12)",
                    "metasysteme",
                    "metasystem",
                    "meta-systeme",
                    "meta-system",
                    "menge",
                    "mengen",
                ),
                {232, 288, 334},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_1/8", "absicht1pro8", "absicht1/8"),
                {272, 379},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Ziele_(19)", "ziele", "maxima", "höhenvorstellungen"),
                {271},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Konkreta_und_Focus_(2)", "konkreta", "focus", "fokus"),
                {250, 269},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Gefühle_(7)", "gefuehle", "emotionen", "gefühle"),
                {243, 283, 284, 285, 286, 305},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("abhängige_Verbundenheit_(90)", "abhaengigkeit", "abhängigkeit"),
                {357},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Karte_Filter_und_Unterscheidung_(1/12)",
                    "karte",
                    "filter",
                    "unterscheidung",
                ),
                {377},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Fundament_(1/19)", "fundament"),
                {356},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Gedanken_sind_Positionen_(17)", "positionen", "gedanken"),
                {249, 317, 323},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Funktionen_Vorstellungen_(16)",
                    "vorstellungen",
                    "vorstellung",
                    "funktionen",
                ),
                {345, 264},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Sollen_Frage_Vorgehensweise_(1/13)",
                    "sollen",
                    "frage",
                    "vorgehensweise",
                ),
                {353, 354},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Ansichten_Standpunkte_(18_17)", "ansichten"),
                {240, 346},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Verbundenheiten_(18)", "verbundenheiten"),
                {252, 299, 300, 336},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Absicht_13_ist_Helfen", "absicht13", "helfen"),
                {370},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Liebe_(7)", "liebe"),
                {8, 9, 28, 208, 221, 330},
                {(121, 122)},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Koalitionen_(10)", "koalitionen"),
                {321},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                ("Impulse_(5)", "impulse"),
                {251, 253, 257, 341},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Triebe_und_Bedürfnisse_(6)",
                    "trieb",
                    "triebe",
                    "bedürfnis",
                    "bedürfnisse",
                ),
                {254},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Reflektion_und_Kategorien_(1/15)",
                    "reflektion",
                    "kategorien",
                ),
                {204, 205, 281},
            ),
            (
                Program.ParametersMain.grundstrukturen,
                (
                    "Modus_und_Sein_(8)",
                    "zustaende",
                    "zustände",
                    "modus",
                    "modi",
                    "sein",
                ),
                {234, 337},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Motive",
                    "motive",
                    "motivation",
                    "motiv",
                    "absicht",
                    "absichten",
                ),
                {10, 18, 42, 167, 168, 149, 230},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Gedanken_sind_Positionen_(17)", "positionen", "gedanken"),
                {249, 276},
            ),
            (
                Program.ParametersMain.menschliches,
                ("Bewusstsein_und_Wahrnehmung", "bewusstsein", "wahrnehmung"),
                {265, 229, 231, 281, 304, 342},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Errungenschaften",
                    "errungenschaften",
                    "ziele",
                    "erhalten",
                ),
                {11, 257, 251},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "evolutionär_erwerben_und_Intelligenz_Kreativität",
                    "evolutionärerwerbenundintelligenz",
                    "intelligenz",
                    "erwerben",
                    "erlernen",
                    "lernen",
                    "evolutionaer",
                    "evolutionär",
                    "kreativität",
                    "kreativitaet",
                    "kreativ",
                ),
                {12, 47, 27, 13, 32},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "brauchen",
                    "benoetigen",
                    "benötigen",
                    "notwendig",
                ),
                {13, 14},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Krankheit",
                    "krankheit",
                    "krankheiten",
                    "pathologisch",
                    "pathologie",
                    "psychiatrisch",
                ),
                {24},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "alpha_beta",
                    "alphabeta",
                    "alpha",
                    "beta",
                    "omega",
                    "sigma",
                ),
                {46},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Anführer",
                    "anfuehrer",
                    "chef",
                ),
                {29, 170},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Manipulation",
                    "manipulation",
                ),
                {153},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Berufe",
                    "berufe",
                    "beruf",
                ),
                {30},
            ),
            (
                Program.ParametersMain.menschliches,
                (
                    "Lösungen",
                    "lösungen",
                    "loesungen",
                    "loesung",
                    "lösungen",
                ),
                {31},
            ),
            (Program.ParametersMain.menschliches, ("Musik", "musik"), {33}),
            (
                Program.ParametersMain.procontra,
                (
                    "ergibt_Sinn",
                    "ergibtsinn",
                    "machtsinn",
                    "sinn",
                ),
                {140},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Veränderung",
                    "veraenderung",
                    "veraendern",
                    "veränderung",
                    "verändern",
                ),
                {142},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "bändigen_kontrollieren",
                    "baendigenkontrollieren",
                    "kontrollieren",
                    "baendigen",
                    "bändigen",
                ),
                {143},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "vereinen",
                    "einheit",
                ),
                {144},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Vorteile",
                    "vorteile",
                    "veraenderungnutzen",
                ),
                {141},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Gegenspieler",
                    "gegenspieler",
                    "antagonist",
                ),
                {137},
            ),
            (
                Program.ParametersMain.procontra,
                ("nervig",),
                {120},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "pro_nutzen",
                    "pronutzen",
                ),
                {117},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Gegenposition",
                    "gegenposition",
                ),
                {116},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Hilfe_erhalten",
                    "hilfeerhalten",
                ),
                {114},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Helfen",
                    "helfen",
                    "hilfe",
                ),
                {115},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Pro",
                    "pro",
                    "dafür",
                    "dafuer",
                ),
                {17, 48},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "nicht_miteinander_auskommen",
                    "nichtauskommen",
                ),
                {123},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "nicht_dagegen",
                    "nichtdagegen",
                ),
                {124},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "kein_Gegenteil",
                    "keingegenteil",
                ),
                {125},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "nicht_dafür",
                    "nichtdafuer",
                ),
                {126},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Hilfe_nicht_gebrauchen",
                    "hilfenichtgebrauchen",
                ),
                {127},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "nicht_helfen_können",
                    "nichthelfenkoennen",
                ),
                {128},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "nicht_abgeneigt",
                    "nichtabgeneigt",
                ),
                {129},
            ),
            (
                Program.ParametersMain.procontra,
                ("unmotivierbar",),
                {130},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "contra",
                    "dagegen",
                ),
                {15, 26},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Gegenteil",
                    "gegenteil",
                ),
                {100, 101, 222},
            ),
            (
                Program.ParametersMain.procontra,
                (
                    "Harmonie",
                    "harmonie",
                ),
                {102, 103},
            ),
            (Program.ParametersMain.licht, (), {20, 27, 313}),
            (
                Program.ParametersMain.procontra,
                (
                    Primzahlkreuz_pro_contra_strs[0],
                    "primzahlkreuz",
                ),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primzahlkreuzprocontra"},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    Primzahlkreuz_pro_contra_strs[0],
                    "primzahlkreuz",
                ),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primzahlkreuzprocontra"},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "in_ReTa",
                    "inreta",
                ),
                {209, 210},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Vorzeichen",
                    "vorzeichen",
                ),
                {118, 119},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Primzahlen",
                    "primzahlen",
                    "vielfache",
                    "vielfacher",
                ),
                {19},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Anwendung_der_Sonnen_und_Monde",
                    "anwendungdersonnenundmonde",
                    "anwendungdersonnen",
                    "anwendungenfuermonde",
                ),
                {22},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Zählungen",
                    "zählungen",
                    "zaehlung",
                    "zaehlungen",
                    "zählung",
                ),
                {25, 45, 169, 188},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Jura",
                    "jura",
                    "gesetzeslehre",
                    "recht",
                ),
                {34},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Vollkommenheit_des_Geistes",
                    "vollkommenheit",
                    "geist",
                ),
                {35},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Gestirn",
                    "gestirn",
                    "mond",
                    "sonne",
                    "planet",
                ),
                {64, 154},
                set(),
                set(),
                set(),
            ),
            (
                Program.ParametersMain.bedeutung,
                ("Konjunktiv_Wurzelbildung", "konjunktiv", "wurzel"),
                {106},
            ),
            (
                Program.ParametersMain.bedeutung,
                (
                    "Mechanismen_der_Züchtung",
                    "mechanismen",
                    "wesen",
                    "zuechtung",
                    "züchtung",
                    "züchten",
                    "zuechten",
                ),
                {107, 108, 109},
            ),
            (
                Program.ParametersMain.gebrochengalaxie,
                set([str(a) for a in range(2, gebrochenSpaltenMaximumPlus1)]),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set([str(a) for a in range(2, gebrochenSpaltenMaximumPlus1)]),
            ),
            (
                Program.ParametersMain.gebrochenuniversum,
                set([str(a) for a in range(2, gebrochenSpaltenMaximumPlus1)]),
                set(),
                set(),
                set(),
                set(),
                set(),
                set([str(a) for a in range(2, gebrochenSpaltenMaximumPlus1)]),
            ),
            (Program.ParametersMain.symbole, (), {36, 37}),
            # (
            #    Program.ParametersMain.Multiplikationen,
            #    allowedPrimNumbersForCommand,
            #    set(),
            #    set(),
            #    (
            #        lambda: {  # nur noch ein Platzhalter
            #            None,
            #        },
            #    ),
            # ),
            (
                Program.ParametersMain.konzept,
                (
                    "Weisheit_etc",
                    "weisheit",
                    "metaweisheit",
                    "meta-weisheit",
                    "idiot",
                    "weise",
                    "optimal",
                    "optimum",
                ),
                {112},
                {(40, 41)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Dein_Recht_bekommen",
                    "rechte",
                    "recht",
                    "selbstgerecht",
                ),
                set(),
                {(291, 292)},
            ),
            (
                Program.ParametersMain.konzept,
                ("unterlegen_überlegen", "unterlegen", "ueberlegen"),
                set(),
                {(380, 381)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Ehrlichkeit_und_Streit", "streit", "ehrlichkeit"),
                set(),
                {(375, 376)},
            ),
            (
                Program.ParametersMain.konzept2,
                ("Würdig", "wuerdig", "würdig"),
                set(),
                {(373, 374)},
            ),
            (
                Program.ParametersMain.konzept2,
                ("Regel_vs_Ausnahme", "regel", "ausnahme"),
                set(),
                {(371, 372)},
            ),
            (
                Program.ParametersMain.konzept2,
                (
                    "Filterart_Widrigkeit",
                    "filterart",
                    "widrigkeit",
                ),
                {331, 335},
            ),
            (
                Program.ParametersMain.konzept2,
                (
                    "Werte",
                    "werte",
                ),
                set(),
                {(360, 361)},
            ),
            (
                Program.ParametersMain.konzept2,
                ("Gutartigkeits-Egoismus", "position", "gutesreziprok"),
                set(),
                {(362, 363)},
            ),
            (
                Program.ParametersMain.konzept2,
                ("Reflektieren_Erkenntnis-Erkennen", "reflektieren", "erkenntnis"),
                set(),
                {(364, 365)},
            ),
            (
                Program.ParametersMain.konzept2,
                ("Vertrauen_wollen", "vertrauenwollen"),
                set(),
                {(366, 367)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "einklinken_vertrauen_anprangern",
                    "einklinken",
                    "vertrauenerhalten",
                    "anprangern",
                ),
                set(),
                {(368, 369)},
            ),
            (
                Program.ParametersMain.konzept2,
                (
                    "Ausrichten_Einrichten",
                    "einrichten",
                    "ausrichten",
                ),
                set(),
                {(358, 359)},
            ),
            (
                Program.ParametersMain.konzept2,
                (
                    "Toleranz_Respekt_Akzeptanz_Willkommen",
                    "toleranz",
                    "respekt",
                    "akzeptanz",
                    "willkommen",
                ),
                set(),
                # {(359, 360)},
                {(62, 63)},
            ),
            (
                Program.ParametersMain.konzept,
                ("familiebrauchen",),
                set(),
                {(279, 280)},
            ),
            (
                Program.ParametersMain.konzept,
                ("ego", "bescheiden"),
                set(),
                {(277, 278)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Selbstsucht_Ichsucht_etc", "selbstsucht", "ichsucht"),
                set(),
                {(274, 275)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Forschen_Erfinden_Einklinken",
                    "wissenschaft",
                    "forschen",
                    "einklinken",
                    "erfinden",
                ),
                set(),
                {(258, 259)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Kooperation_vs_Arsch", "arschloch", "kooperation", "arsch"),
                set(),
                {(245, 246)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Liebe_usw", "liebe", "zuneigung"),
                set(),
                {(247, 248)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Selbstlosigkeit_Ichlosigkeit_etc", "selbstlos", "ichlos"),
                set(),
                {(238, 239)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "variationsreich_eintönig",
                    "eintönig",
                    "eintoenig",
                    "variationsreich",
                ),
                set(),
                {(236, 237)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Zuneigung_Abneigung",
                    "abgeneigt",
                    "zugewandt",
                    "reserviert",
                    "zugeneigt",
                ),
                set(),
                {(199, 200)},
            ),
            (
                Program.ParametersMain.menschliches,
                ("ehrlich vs höflich", "ehrlich", "höflich", "hoeflich"),
                set(),
                {(224, 225)},
            ),
            # (
            #    Program.ParametersMain.konzept,
            #    ("delegieren", "ansammlung"),
            #    set(),
            #    {(227, 228)},
            # ),
            (
                Program.ParametersMain.konzept,
                ("ehrlich vs höflich", "ehrlich", "höflich", "hoeflich"),
                set(),
                {(224, 225)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Tragweite", "tragweite"),
                set(),
                {(211, 212)},
            ),
            (
                Program.ParametersMain.konzept,
                ("wertvoll", "wertlos"),
                set(),
                {(186, 187)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Götter_Propheten_Familien_Freunde",
                    "familiaer",
                    "goettlich",
                    "freunde",
                    "propheten",
                ),
                set(),
                {(184, 185)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "sanft_vs_hart",
                    "sanft",
                    "hart",
                ),
                set(),
                {(159, 160), (161, 162)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "vereinen_vs_verbinden",
                    "vereinenverbinden",
                    "vereinen",
                    "verbinden",
                    "einheit",
                    "verbindung",
                ),
                set(),
                {(133, 134)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "ähnlich",
                    "aehnlich",
                ),
                {220},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "gut_böse_lieb_schlecht",
                    "gut",
                    "böse",
                    "boese",
                    "lieb",
                    "schlecht",
                ),
                {52, 53},
                {(38, 39)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Sinn_und_Zweck_des_Lebens", "sinn", "zweck", "bedeutung"),
                {88, 189},
                {(181, 182)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Zeit_vs_Raum",
                    "zeit",
                    "raum",
                    "zeitlich",
                    "räumlich",
                ),
                set(),
                {(49, 50)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "egalitär_vs_autoritär",
                    "egalitaerautoritaer",
                    "egalitaer",
                    "autoritaer",
                    "egalitär",
                    "autoritär",
                ),
                set(),
                {(163, 164)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Meinungen_und_Ruf",
                    "meinungen",
                    "anderemenschen",
                    "ruf",
                ),
                set(),
                {(60, 61)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Meinungsintelligenz", "meinungsintelligenz", "ursprungsintelligenz"),
                set(),
                {(151, 152)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Sittlichkeit", "sittlichkeit", "annaehrerung"),
                set(),
                {(179, 180)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Führung", "führung", "fuehrung"),
                set(),
                {(173, 174)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Durchleuchten", "durchleuchten", "erleuchten"),
                set(),
                {(177, 178)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Fördern_Sensiblisieren_und_Gedeihen",
                    "foerdern",
                    "fördern",
                    "begrenzen",
                    "sensibilisieren",
                    "gedeihen",
                    "verderben",
                ),
                set(),
                {(175, 176)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Überheblichkeit",
                    "überheblich",
                    "ueberheblichkeit",
                    "ueberheblich",
                    "überheblichkeit",
                ),
                set(),
                {(171, 172)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Polung_der_Liebe",
                    "liebepolung",
                ),
                set(),
                {(121, 122)},
            ),
            (
                Program.ParametersMain.konzept,
                (
                    "Egoismus_vs_Altruismus",
                    "egoismus",
                    "altruismus",
                    "egoist",
                    "altruist",
                ),
                {136},
                {(66, 67)},
            ),
            (
                Program.ParametersMain.konzept,
                ("kausal", "geltung", "genese"),
                set(),
                {(110, 111)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Gleichheit", "gleich"),
                set(),
                {(192, 193)},
            ),
            (
                Program.ParametersMain.konzept,
                ("Überleben", "ueberleben"),
                set(),
                {(194, 195)},
            ),
            (Program.ParametersMain.inkrementieren, set(), {43, 54, 74, 95}),
            (Program.ParametersMain.inkrementieren, ("um1",), {155}),
            (Program.ParametersMain.inkrementieren, ("um2",), {156}),
            (Program.ParametersMain.inkrementieren, ("um3",), {157}),
            (
                Program.ParametersMain.inkrementieren,
                (
                    "warum_Transzendentalie_=_Strukturgroesse_=_Charakter",
                    "warumtranszendentaliezustrukturgroesseundcharakter",
                ),
                {4, 54, 5, 165},
            ),
            (
                Program.ParametersMain.inkrementieren,
                (
                    "warum_Transzendentalie_=_Komplexität_von_Michael_Commons",
                    "warumtranszendentaliegleichkomplexitaet",
                ),
                {65, 5, 166},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Rahmen-Bedingungen", "rahmen"),
                {226},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Motive_gleichförmige_Polygone", "motivgleichfoermig"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primMotivGleichf"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Struktur_gleichförmige_Polygone", "strukturgleichfoermig"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primStrukGleichf"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Motive_Sternpolygone", "motivstern"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primMotivStern"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Struktur_Sternpolygone", "strukturstern"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primStrukStern"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Motiv_Sternpolygon_gebrochen-rational", "motivgebrstern"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primMotivSternGebr"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Struktur_Sternpolyon_gebrochen-rational", "strukgebrstern"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primStrukSternGebr"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("Motiv_gleichförmige_Polygone_gebrochen-rational", "motivgebrgleichf"),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primMotivGleichfGebr"},
            ),
            (
                Program.ParametersMain.primvielfache,
                (
                    "Struktur_gleichförmige_Polygone_gebrochen-rational",
                    "strukgebrgleichf",
                ),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"primStrukGleichfGebr"},
            ),
            (
                Program.ParametersMain.primvielfache,
                ("beschrieben",),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                set(),
                {"PrimCSV"},
            ),
        ]
        Program.paraNdataMatrix = paraNdataMatrix

        """
        paraNdataMatrix4onlyGenerated: dict = {
            "primMotivGleichf": (
                ("Primzahlvielfache", "primvielfache"),
                ("Motive_gleichförmige_Polygone", "motivgleichfoermig"),
            ),
            "primStrukGleichf": (
                ("Primzahlvielfache", "primvielfache"),
                ("Struktur_gleichförmige_Polygone", "strukturgleichfoermig"),
            ),
            "primMotivStern": (
                ("Primzahlvielfache", "primvielfache"),
                ("Motive_Sternpolygone", "motivstern"),
            ),
            "primStrukStern": (
                ("Primzahlvielfache", "primvielfache"),
                ("Struktur_Sternpolygone", "strukturstern"),
            ),
            "primStrukGebrRat": (
                ("Primzahlvielfache", "primvielfache"),
                ("Struktur_gebrochen-rational", "strukturgebrochenrational"),
            ),
            "PrimCSV": (("Primzahlvielfache", "primvielfache"), ("beschrieben",)),
        }
        """

        Program.kombiParaNdataMatrix: OrderedDict[int, tuple[str]] = OrderedDict(
            {
                1: (
                    "Lebewesen",
                    "tiere",
                    "tier",
                    "lebewesen",
                ),
                2: ("Berufe", "berufe", "beruf"),
                3: (
                    "Kreativität_und_Intelligenz",
                    "kreativität",
                    "intelligenz",
                    "kreativitaet",
                ),
                4: (
                    "Liebe",
                    "liebe",
                ),
                7: (
                    "Männer",
                    "männer",
                    "maenner",
                    "frauen",
                ),
                8: (
                    "Persönlichkeit_evolutionär_erwerben",
                    "evolution",
                    "erwerben",
                    "persoenlichkeit",
                    "persönlichkeit",
                ),
                9: (
                    "Religion",
                    "religion",
                    "religionen",
                ),
                10: ("Motive_Ziele", "motivation", "motive", "ziele", "ziel", "motive"),
                12: (
                    "Emotionen",
                    "emotionen",
                    "gefuehle",
                    "gefühle",
                    "emotion",
                    "gefühl",
                    "gefühle",
                ),
                13: ("Personen", "personen", "berühmtheiten", "beruehmtheiten"),
                16: (
                    "Wirtschaftssysteme",
                    "wirtschaftssystem",
                    "wirtschaftssysteme",
                    "kombinierteswirtschaftssystem",
                    "kombiniertewirtschaftssysteme",
                ),
            }
        )

        Program.kombiParaNdataMatrix2: OrderedDict[int, tuple[str]] = OrderedDict(
            {
                1: (
                    "Lebewesen",
                    "tiere",
                    "tier",
                    "lebewesen",
                ),
                2: ("Berufe", "berufe", "beruf"),
                # 3: (
                #    "Kreativität_und_Intelligenz",
                #    "kreativität",
                #    "intelligenz",
                #    "kreativitaet",
                # ),
                # 4: (
                #    "Liebe",
                #    "liebe",
                # ),
                5: (
                    "Transzendentalien_Strukturalien",
                    "transzendenz",
                    "transzendentalien",
                    "strukturalien",
                    "alien",
                ),
                6: ("Primzahlkreuz", "leibnitz", "primzahlkreuz"),
                # 7: (
                #    "Männer",
                #    "männer",
                #    "maenner",
                #    "frauen",
                # ),
                8: (
                    "Persönlichkeit_evolutionär_erwerben",
                    "evolution",
                    "erwerben",
                    "persoenlichkeit",
                    "persönlichkeit",
                ),
                # 9: (
                #    "Religion",
                #    "religion",
                #    "religionen",
                # ),
                10: ("Motive_Ziele", "motivation", "motive", "ziele", "ziel", "motive"),
                11: ("analytische_Ontologie", "analytischeontologie", "ontologie"),
                # 12: (
                #    "Emotionen",
                #    "emotionen",
                #    "gefuehle",
                #    "gefühle",
                #    "emotion",
                #    "gefühl",
                #    "gefühle",
                # ),
                # 13: ("Personen", "personen", "berühmtheiten", "beruehmtheiten"),
                14: (
                    "Mechanismen_der_Zuechtung",
                    "mechanismen",
                    "wesen",
                    "zuechten",
                    "züchten",
                ),
                15: (
                    "Gegentranszendentalien",
                    "gegentranszendentalien",
                    "gegenstrukturalien",
                ),
                # 16: (
                #    "Wirtschaftssysteme",
                #    "wirtschaftssystem",
                #    "wirtschaftssysteme",
                #    "kombinierteswirtschaftssystem",
                #    "kombiniertewirtschaftssysteme",
                # ),
                17: ("Maschinen", "maschinen", "geräte", "geraete"),
                18: ("Geist", "geist"),
                19: ("Bewusstsein", "bewusstsein"),
            }
        )

        self.kombiReverseDict: dict = {}
        for key, value in Program.kombiParaNdataMatrix.items():
            for valuesInValuess in value:
                self.kombiReverseDict[valuesInValuess] = key

        self.kombiReverseDict2: dict = {}
        for key, value in Program.kombiParaNdataMatrix2.items():
            for valuesInValuess in value:
                self.kombiReverseDict2[valuesInValuess] = key

        allValues = [
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
            OrderedSet(),
        ]
        for possibleCommands in paraNdataMatrix:
            for commandValue, aAllValue in zip(possibleCommands[2:], allValues):
                try:
                    aAllValue |= commandValue
                except TypeError:
                    pass

        """
        Folgende Schleife ist eigentlich unnötig.
        Sie ist für bool Werte da, wenn Sachen generiert werden.
        Ich brauche aber gerade den bool wert gar nicht mehr, weil es in
        diesem Fall auch anders geht, aber für die Zukunft kann das hilfreich sein.
        Also lasse ich es mal stehen!

        for possibleCommands in paraNdataMatrix:
            for commandValue, aAllValue in zip(possibleCommands[6:], allValues[4:]):
                aAllValue += [commandValue]
        # allValues[1] = allValues[2]
        """
        allValues[2] = set((int(pNum) for pNum in allowedPrimNumbersForCommand))
        allValues[3] = set(Program.kombiParaNdataMatrix.keys())
        allValues[5] = set(range(2, gebrochenSpaltenMaximumPlus1))
        allValues[6] = set(range(2, gebrochenSpaltenMaximumPlus1))
        allValues[8] = set(Program.kombiParaNdataMatrix2.keys())

        """
        self.paraDictGenerated = {}
        self.paraDictGenerated4htmlTags = {}
        for key, value in paraNdataMatrix4onlyGenerated.items():
            for firstParameter in value[0][1:]:
                for secondParameter in value[1][1:]:
                    self.paraDictGenerated[(firstParameter, secondParameter)] = key
            self.paraDictGenerated4htmlTags[(value[0][0], value[1][0])] = key
            allValues[7] |= {key}
        """

        paraNdataMatrix += [
            (
                Program.ParametersMain.alles,
                (),
                *allValues,
            )
        ]
        """
        Hier wird erreicht, dass beide Dictionaries stückweise aufgefüllt werden.
        Aus den 3 voran gegangen Datenstrukturen werden 2 Dicts gemacht.
        """
        self.paraMainDict, self.paraDict = {}, {}
        for parameterEntry in paraNdataMatrix:
            into = intoParameterDatatype(
                parameterEntry[0],
                parameterEntry[1],
                tuple(
                    parameterEntryElement
                    for parameterEntryElement in parameterEntry[2:]
                ),
            )
            self.paraDict, self.dataDict = mergeParameterDicts(
                self.paraMainDict,
                self.paraDict,
                self.dataDict,
                *into,
            )

        self.dataDict[3] = Program.kombiParaNdataMatrix
        self.dataDict[8] = Program.kombiParaNdataMatrix2

        # alxp(self.paraDictGenerated)
        # alxp("-|-|")
        # alxp(self.paraDictGenerated4htmlTags)
        # alxp("||-|")
        # alxp(self.paraDict)
        # alxp("--|-")
        # alxp(self.dataDict)
        # alxp("--||")
        self.tables.dataDict = self.dataDict

    def parametersToCommandsAndNumbers(
        self, argv, neg=""
    ) -> Iterable[Union[set, set, set, list]]:
        """Parameter in der Shell werden hier vorverarbeitet.
        Die Paraemter führen dazu, dass Variablen gesetzt werden, z.B.
        eine Menge die als Befehl kodiert, welche Zeilen und eine die kodiert
        welche Spaltennummer ausgegeben werden sollen.
        Außerdem welche extra Tabellen geladen werden sollen.

        return paramLines, rowsAsNumbers, rowsOfcombi

        @type  argv: list
        @param argv: Programmparamenter
        @type  neg: str
        @param neg: MinusZeichen davor ?
        @rtype: set, set, set
        @return: Zeilen, Spalten, Spalten anderer Tabellen
        """
        global infoLog, shellRowsAmount  # , puniverseprims
        if len(argv) == 1 and neg == "":
            cliout("Versuche Parameter -h")
        spaltenreihenfolgeundnurdiese: tuple = ()
        puniverseprims_only: set = OrderedSet()
        rowsAsNumbers: set = set()
        paramLines: set = OrderedSet()
        self.bigParamaeter: list = []
        self.__willBeOverwritten_rowsOfcombi: set = OrderedSet()
        generRows = OrderedSet()
        # for arg in argv[1:]:
        #    elif (
        #                arg[2 : 2 + len("spaltenreihenfolgeundnurdiese=")]
        #                == "spaltenreihenfolgeundnurdiese="
        #    ):
        for arg in argv[1:]:
            if len(arg) > 0 and arg[0] == "-":
                if (
                    len(arg) > 1
                    and arg[1] == "-"
                    and len(self.bigParamaeter) > 0
                    and self.bigParamaeter[-1] == "zeilen"
                ):
                    if arg[2:7] == "alles" and len(neg) == 0:
                        paramLines.add("all")
                        self.obZeilenBereicheAngegeben = True
                    if arg[2:7] == "alles" and len(neg) != 0:
                        pass
                    elif arg[2:7] == "zeit=":
                        self.obZeilenBereicheAngegeben = True
                        for subpara in arg[7:].split(","):
                            if neg + "heute" == subpara:
                                paramLines.add("=")
                            elif neg + "gestern" == subpara:
                                paramLines.add("<")
                            elif neg + "morgen" == subpara:
                                paramLines.add(">")
                    elif arg[2:11] == "zaehlung=":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "":
                            paramLines |= (
                                self.tables.getPrepare.parametersCmdWithSomeBereich(
                                    arg[11:], "n", "", True
                                )
                            )
                            x("paraLi", paramLines)
                    elif arg[2:15] == "hoehemaximal=":
                        if arg[15:].isdecimal():
                            self.tables.textHeight = abs(int(arg[15:]))
                    elif arg[2:6] == "typ=":
                        self.obZeilenBereicheAngegeben = True
                        for word in arg[6:].split(","):
                            if word == neg + "sonne":
                                paramLines.add("sonne")
                            elif word == neg + "schwarzesonne":
                                paramLines.add("schwarzesonne")
                            elif word == neg + "planet":
                                paramLines.add("planet")
                            elif word == neg + "mond":
                                paramLines.add("mond")
                    elif arg[2 : 2 + len("potenzenvonzahlen=")] == "potenzenvonzahlen=":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "" or True:
                            angabe = arg[2 + len("potenzenvonzahlen=") :]
                            paramLines |= (
                                self.tables.getPrepare.parametersCmdWithSomeBereich(
                                    angabe, "^", neg, keineNegBeruecksichtigung=False
                                )
                            )
                    elif arg[2:21] == "vielfachevonzahlen=":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "":
                            paramLines |= (
                                self.tables.getPrepare.parametersCmdWithSomeBereich(
                                    arg[21:], "b", neg, keineNegBeruecksichtigung=True
                                )
                            )
                    elif arg[2:20] == "primzahlvielfache=":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "":
                            zahlenMenge = BereichToNumbers2(
                                arg[2 + len("primzahlvielfache=") :]
                            )
                            for zahl in zahlenMenge:
                                paramLines.add(str(zahl) + "p")
                    elif self.oberesMaximum(arg):
                        pass
                    elif arg[2:27] == "vorhervonausschnittteiler":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "":
                            paramLines |= (
                                self.tables.getPrepare.parametersCmdWithSomeBereich(
                                    "1", "w", neg, keineNegBeruecksichtigung=True
                                )
                            )
                    elif arg[2:22] == "vorhervonausschnitt=":
                        self.obZeilenBereicheAngegeben = True
                        if neg == "":
                            paramLines |= (
                                self.tables.getPrepare.parametersCmdWithSomeBereich(
                                    arg[22:], "a", neg, keineNegBeruecksichtigung=True
                                )
                            )
                    elif arg[2:38] == "nachtraeglichneuabzaehlungvielfache=":
                        self.obZeilenBereicheAngegeben = True
                        paramLines |= (
                            self.tables.getPrepare.parametersCmdWithSomeBereich(
                                arg[38:], "y", neg
                            )
                        )
                    elif arg[2:29] == "nachtraeglichneuabzaehlung=":
                        self.obZeilenBereicheAngegeben = True
                        paramLines |= (
                            self.tables.getPrepare.parametersCmdWithSomeBereich(
                                arg[29:], "z", neg
                            )
                        )
                    elif len(neg) > 0:
                        from LibRetaPrompt import zeilenParas

                        cliout(
                            'Den Neben-Parameter "'
                            + arg
                            + '" gibt es hier nicht für den Hauptparameter "-'
                            + self.bigParamaeter[-1]
                            + '".'
                            + " Möglich sind: "
                            + ", ".join(zeilenParas)
                        )
                elif (
                    len(arg) > 1
                    and arg[1] == "-"
                    and len(self.bigParamaeter) > 0
                    and self.bigParamaeter[-1] == "ausgabe"
                ):  # unteres Kommando
                    # print(arg[2:])
                    if self.breiteBreitenSysArgvPara(arg[2:], neg):
                        pass
                    elif (
                        arg[2 : 2 + len("keineueberschriften")] == "keineueberschriften"
                    ):
                        self.tables.keineUeberschriften = True
                    elif arg[2 : 2 + len("keinenummerierung")] == "keinenummerierung":
                        self.tables.nummeriere = False
                    elif arg[2 : 2 + len("keineleereninhalte")] == "keineleereninhalte":
                        self.keineleereninhalte = True
                        self.tables.keineleereninhalte = True
                    elif (
                        arg[2 : 2 + len("spaltenreihenfolgeundnurdiese=")]
                        == "spaltenreihenfolgeundnurdiese="
                    ):
                        spaltenreihenfolgeundnurdiese = tuple(
                            BereichToNumbers2(
                                arg[2 + len("spaltenreihenfolgeundnurdiese=") :]
                            )
                        )
                    elif arg[2:6] == "art=":
                        outputtype = arg[(arg.find("=") + 1) :]
                        if outputtype == "shell":
                            self.tables.outType = OutputSyntax()
                        elif outputtype == "csv":
                            self.tables.outType = csvSyntax()
                            self.tables.getOut.oneTable = True
                            self.breiteBreitenSysArgvPara("breite=0", "")
                        elif outputtype == "bbcode":
                            self.htmlOrBBcode = True
                            self.tables.outType = bbCodeSyntax()
                        elif outputtype == "html":
                            self.tables.outType = htmlSyntax()
                            self.htmlOrBBcode = True
                        elif outputtype == "emacs":
                            self.tables.getOut.oneTable = True
                            self.tables.outType = emacsSyntax()
                            self.breiteBreitenSysArgvPara("breite=0", "")
                        elif outputtype == "markdown":
                            self.tables.outType = markdownSyntax()
                            self.tables.getOut.oneTable = True
                            self.breiteBreitenSysArgvPara("breite=0", "")
                    elif arg[2:] in ["nocolor", "justtext"] and neg == "":
                        self.tables.getOut.color = False
                    elif (
                        arg[2:] in ["endlessscreen", "endless", "dontwrap", "onetable"]
                        and neg == ""
                    ):
                        self.tables.getOut.oneTable = True
                    elif len(neg) == 0:
                        cliout(
                            'Den Neben-Parameter "'
                            + arg
                            + '" gibt es hier nicht für den Hauptparameter "-'
                            + self.bigParamaeter[-1]
                            + '".'
                        )
                else:  # oberes Kommando
                    if arg[1:] in ["zeilen", "spalten", "kombination", "ausgabe"]:
                        self.bigParamaeter += [arg[1:]]
                    elif arg[1:] in ["debug"]:
                        infoLog = True
                    elif arg[1:] in ["h", "help"] and neg == "":
                        self.helpPage()

        if not self.tables.getOut.oneTable:
            shellRowsAmount, _, _, _ = getTextWrapThings()

            self.tables.textWidth = (
                self.tables.textWidth
                if shellRowsAmount > self.tables.textWidth + 7 or shellRowsAmount <= 0
                else shellRowsAmount - 7
            )
        self.tables.ifZeilenSetted = self.obZeilenBereicheAngegeben
        return (
            paramLines,
            rowsAsNumbers,
            self.__willBeOverwritten_rowsOfcombi,
            spaltenreihenfolgeundnurdiese,
            puniverseprims_only,
            generRows,
        )

    def helpPage(self):
        global folder
        retaHilfe()

    def bringAllImportantBeginThings(self, argv) -> tuple:
        """Einlesen der ersten Tabelle "religion.csv" zu self.relitable
        aller anderen csv dateien
        Parameter werden in Befehle und Nummernlisten gewandelt
        csv Dateien werden angehangen an self.relitable


        @rtype: tuple(int,set,set,list,set,list,set,list,list)
        @return: Spaltenanzahl, Zeilen Ja, Zeilen Nein, Religionstabelle, Spalten, weitere Tabelle daneben, spalten weitere Tabelle, weitere Tabelle für wie sql-join, deren spalten
        """
        global folder, shellRowsAmount
        if "Brython" not in sys.version.split():
            place = os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                os.path.basename("./religion.csv"),
            )
        else:
            place = "religion.csv"
        with open(place, mode="r", encoding="utf-8") as csv_file:
            self.relitable: list = []
            # maxi: dict = {}
            # tabneu = np.chararray((len(self.relitable) + 1, self.tables.hoechsteZeile[1024] + 3), itemsize=5000, unicode = True)
            # self.relitable = np.chararray((len(self.relitable) + 1, self.tables.hoechsteZeile[1024] + 3), itemsize=5000, unicode = True)
            for i, col in enumerate(csv.reader(csv_file, delimiter=";")):

                if "--art=bbcode" in self.argv:
                    col = [
                        json.loads(ccc[1:-1])["bbcode"]
                        if ccc[:2] == "|{" and ccc[-2:] == "}|"
                        else ccc
                        for ccc in col
                    ]
                elif "--art=html" in self.argv:
                    col = [
                        json.loads(ccc[1:-1])["html"]
                        if ccc[:2] == "|{" and ccc[-2:] == "}|"
                        else html.escape(ccc, quote=True)
                        for ccc in col
                    ]
                else:
                    col = [
                        json.loads(ccc[1:-1])[""]
                        if ccc[:2] == "|{" and ccc[-2:] == "}|"
                        else ccc
                        for ccc in col
                    ]
                # try:
                #    maxi = { u : max(len(c_),maxi[u]) for u,c_ in enumerate(col)}
                # except:
                #    maxi = { u : len(c_) for u,c_ in enumerate(col)}
                self.relitable += [col]
                # self.relitable[i] = np.array(col, dtype=str)
                if i == 0:
                    self.RowsLen = len(col)

            # avg = maxi.values()
            # avg = sum(avg) / len(avg)
            # x("maxI",avg)
            for egal in range(
                len(self.relitable) + 1, self.tables.hoechsteZeile[1024] + 2
            ):
                self.relitable += [[""] * len(self.relitable[0])]

        # x("tabneu", tabneu)

        self.htmlOrBBcode = False
        self.breiteORbreiten = False
        self.keineleereninhalte = False
        self.tables.keineleereninhalte = False
        (
            paramLines,
            self.rowsAsNumbers,
            self.rowsOfcombi,
            spaltenreihenfolgeundnurdiese,
            self.puniverseprims,
            self.generRows,
        ) = self.parametersToCommandsAndNumbers(argv)
        (
            paramLinesNot,
            self.rowsAsNumbersNot,
            self.rowsOfcombiNot,
            spaltenreihenfolgeundnurdieseNot,
            self.puniverseprimsNot,
            self.generRowsNot,
        ) = self.parametersToCommandsAndNumbers(argv, "-")
        self.dataDict: list = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
        self.spaltenTypeNaming: namedtuple = namedtuple(
            "SpaltenTyp",
            "ordinary generated1 concat1 kombi1 boolAndTupleSet1 gebroUni1 gebrGal1 generated2 kombi2 ordinaryNot generate1dNot concat1Not kombi1Not boolAndTupleSet1Not gebroUni1Not gebrGal1Not generated2Not kombi2Not",
        )
        self.spaltenTypeNaming = self.spaltenTypeNaming(
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, 8),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8),
        )

        # self.spaltenArtenNameKey_SpaltenArtenTupleVal_4Key4otherDict = {
        #    "ordinary": (0, 0),
        #    "generated1": (0, 1),
        #    "concat1": (0, 2),
        #    "kombi1": (0, 3),
        #    "ordinaryNot": (1, 0),
        #    "generate1dNot": (1, 1),
        #    "concat1Not": (1, 2),
        #    "kombi1Not": (1, 3),
        # }
        self.spaltenArtenKey_SpaltennummernValue = {
            (0, 0): OrderedSet(),
            (0, 1): OrderedSet(),
            (0, 2): OrderedSet(),
            (0, 3): OrderedSet(),
            (0, 4): OrderedSet(),
            (0, 5): OrderedSet(),
            (0, 6): OrderedSet(),
            (0, 7): OrderedSet(),
            (0, 8): OrderedSet(),
            (1, 0): OrderedSet(),
            (1, 1): OrderedSet(),
            (1, 2): OrderedSet(),
            (1, 3): OrderedSet(),
            (1, 4): OrderedSet(),
            (1, 5): OrderedSet(),
            (1, 6): OrderedSet(),
            (1, 7): OrderedSet(),
            (1, 8): OrderedSet(),
        }

        self.storeParamtersForColumns()
        self.produceAllSpaltenNumbers()
        if self.htmlOrBBcode and not self.breiteORbreiten:
            shellRowsAmount = 0
            self.tables.textWidth = 0

        paramLines, paramLinesNot = self.tables.getPrepare.deleteDoublesInSets(
            paramLines, paramLinesNot
        )
        self.rowsAsNumbers = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.ordinary
        ]
        self.generRows = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.generated1
        ]
        self.puniverseprims = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.concat1
        ]
        self.rowsOfcombi = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.kombi1
        ]
        self.rowsOfcombi2 = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.kombi2
        ]
        self.onlyGenerated = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.boolAndTupleSet1
        ]
        self.gebrUni = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.gebroUni1
        ]
        self.gebrGal = self.spaltenArtenKey_SpaltennummernValue[
            self.spaltenTypeNaming.gebrGal1
        ]
        ones = []
        for a in self.onlyGenerated:
            if len(a) == 1:
                ones += a
        self.tables.getConcat.ones = ones

        for gebrUniva in self.gebrUni:
            self.tables.gebrUnivSet.add(gebrUniva)
        for prims in self.puniverseprims:
            self.tables.primUniversePrimsSet.add(prims)

        if len(self.rowsOfcombi) > 0:
            paramLines.add("ka")
        if len(self.rowsOfcombi2) > 0:
            paramLines.add("ka2")
        self.tables.generRows = self.generRows
        self.tables.getPrepare.rowsAsNumbers = self.rowsAsNumbers
        self.tables.getOut.rowsAsNumbers = self.rowsAsNumbers

        self.tables.SpaltenVanillaAmount = len(self.rowsAsNumbers)

        CsvTheirsSpalten: dict = {}
        for i, input1 in enumerate(
            [
                self.puniverseprims,
                self.gebrUni,
                self.gebrGal,
                self.gebrUni,
                self.gebrGal,
            ],
            start=1,
        ):
            (
                self.relitable,
                rowsAsNumbers,
                CsvTheirsSpalten[i],
            ) = self.tables.getConcat.readConcatCsv(
                self.relitable, self.rowsAsNumbers, input1, i
            )
        primSpalten = CsvTheirsSpalten[1]
        gebrUnivSpalten = CsvTheirsSpalten[2]
        gebrGalSpalten = CsvTheirsSpalten[3]
        gebrUnivSpalten2 = CsvTheirsSpalten[4]
        gebrGalSpalten2 = CsvTheirsSpalten[5]

        (
            finallyDisplayLinesEarly,
            headingsAmountEarly,
            newerTableEarly,
            numlenEarly,
            rowsRangeEarly,
        ) = self.tables.getPrepare.prepare4out_beforeForLoop_SpaltenZeilenBestimmen(
            self.relitable, paramLines, paramLinesNot
        )
        zeilenliste = list(finallyDisplayLinesEarly)
        zeilenliste.sort()
        self.tables.lastLineNumber = zeilenliste[-1]

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concatVervielfacheZeile(
            self.relitable, self.rowsAsNumbers
        )
        self.relitable, self.rowsAsNumbers = self.tables.getConcat.concatModallogik(
            self.relitable, self.tables.generRows, self.rowsAsNumbers
        )
        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concatPrimCreativityType(
            self.relitable, self.rowsAsNumbers
        )

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concatGeistEmotionEnergieMaterieTopologie(
            self.relitable, self.rowsAsNumbers
        )

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concatMondExponzierenLogarithmusTyp(
            self.relitable, self.rowsAsNumbers
        )

        paraTextNamen = {}
        for text in self.spaltenArtenKey_SpaltennummernValue[(0, 7)]:
            paraTextNamen[text] = [self.dataDict[7][text]]

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concat1RowPrimUniverse2(
            self.relitable,
            self.rowsAsNumbers,
            self.spaltenArtenKey_SpaltennummernValue[(0, 7)],
            paraTextNamen,
        )

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concat1PrimzahlkreuzProContra(
            self.relitable,
            self.rowsAsNumbers,
            self.spaltenArtenKey_SpaltennummernValue[(0, 7)],
            Program.ParametersMain,
        )

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.concatLovePolygon(self.relitable, self.rowsAsNumbers)
        (
            self.relitable,
            rowsAsNumbers,
        ) = self.tables.getConcat.spalteFuerGegenInnenAussenSeitlichPrim(
            self.relitable, self.rowsAsNumbers
        )

        couplesX = []
        for a in self.onlyGenerated:
            if len(a) == 2:
                couplesX += [a]

        (
            self.relitable,
            self.rowsAsNumbers,
        ) = self.tables.getConcat.spalteMetaKontretTheorieAbstrakt_etc_1(
            self.relitable, self.rowsAsNumbers, couplesX
        )

        self.tables.getMainTable.createSpalteGestirn(self.relitable, self.rowsAsNumbers)

        if len(self.rowsOfcombi) > 0:
            (
                animalsProfessionsTable,
                self.relitable,
                kombiTable_Kombis,
                maintable2subtable_Relation,
            ) = self.tables.getCombis.readKombiCsv(
                self.relitable, self.rowsAsNumbers, self.rowsOfcombi, "kombi.csv"
            )
        else:
            animalsProfessionsTable = []
            kombiTable_Kombis = []
            maintable2subtable_Relation = []

        if len(self.rowsOfcombi2) > 0:
            (
                animalsProfessionsTable2,
                self.relitable,
                kombiTable_Kombis2,
                maintable2subtable_Relation2,
            ) = self.tables.getCombis.readKombiCsv(
                self.relitable, self.rowsAsNumbers, self.rowsOfcombi2, "kombi-meta.csv"
            )
        else:
            animalsProfessionsTable2 = []
            kombiTable_Kombis2 = []
            maintable2subtable_Relation2 = []

        return (
            self.RowsLen,
            paramLines,
            paramLinesNot,
            self.relitable,
            self.rowsAsNumbers,
            animalsProfessionsTable,
            self.rowsOfcombi,
            kombiTable_Kombis,
            maintable2subtable_Relation,
            spaltenreihenfolgeundnurdiese,
            primSpalten,
            gebrUnivSpalten,
            gebrGalSpalten,
            gebrUnivSpalten2,
            gebrGalSpalten2,
            animalsProfessionsTable2,
            kombiTable_Kombis2,
            maintable2subtable_Relation2,
        )

    def oberesMaximumArg(self, arg) -> tuple:
        werte: list[int] = []
        if arg[2:16] == "oberesmaximum=" and arg[16:].isdecimal():
            werte = [int(arg[16:])]
            return werte, True
        elif arg[2:22] == "vorhervonausschnitt=":
            werteList: list[int] = [
                a + 1 for a in BereichToNumbers2(arg[22:], False, 0)
            ]
            werte = [max(w, 1024) for w in werteList]
            return werte, False
        else:
            return werte, False

    def oberesMaximum2(self, argv2) -> Optional[int]:
        try:
            werte: list[int] = [self.tables.hoechsteZeile[1024]]
        except:
            werte: list[int] = []
        for arg in argv2:
            werte += self.oberesMaximumArg(arg)[0]

        return max(werte) if len(werte) > 0 else None

    def oberesMaximum(self, arg) -> bool:
        liste, wahrheitswert = self.oberesMaximumArg(arg)
        if len(liste) == 0 or not wahrheitswert:
            return False
        max_ = max(liste + [self.tables.hoechsteZeile[1024]])
        self.tables.hoechsteZeile = max_
        return True

    @property
    def propInfoLog(self) -> OutputSyntax:
        global Tables, infoLog
        return infoLog

    @propInfoLog.setter
    def propInfoLog(self, value: bool):
        global Tables, infoLog
        infoLog = value

    def __init__(self, argv=[], alternativeShellRowsAmount: Optional[int] = None):
        global Tables, infoLog
        self.argv = argv
        self.allesParameters = 0
        self.tables = Tables(self.oberesMaximum2(argv[1:]))

        self.breiteHasBeenOnceZero: bool = False
        self.obZeilenBereicheAngegeben = False
        if platform.system() == "Windows":
            self.tables.getOut.color = False

        # if "--breite=0" in argv:
        #    self.breiteBreitenSysArgvPara("--breite=0", "")
        self.workflowEverything(argv)

    def workflowEverything(self, argv):
        global infoLog
        (
            self.RowsLen,
            paramLines,
            paramLinesNot,
            self.relitable,
            self.rowsAsNumbers,
            animalsProfessionsTable,
            self.rowsOfcombi,
            kombiTable_Kombis,
            maintable2subtable_Relation,
            spaltenreihenfolgeundnurdiese,
            primSpalten,
            gebrUnivSpalten,
            gebrGalSpalten,
            gebrUnivSpalten2,
            gebrGalSpalten2,
            animalsProfessionsTable2,
            kombiTable_Kombis2,
            maintable2subtable_Relation2,
        ) = self.bringAllImportantBeginThings(argv)

        (
            finallyDisplayLines,
            newTable,
            numlen,
            rowsRange,
            old2newTable,
        ) = self.tables.getPrepare.prepare4out(
            paramLines,
            paramLinesNot,
            self.relitable,
            self.rowsAsNumbers,
            primSpalten=primSpalten,
            gebrUnivSpalten=gebrUnivSpalten,
            gebrGalSpalten=gebrGalSpalten,
            gebrUnivSpalten2=gebrUnivSpalten2,
            gebrGalSpalten2=gebrGalSpalten2,
        )

        if len(self.rowsOfcombi) > 0:
            newTable = self.combiTableWorkflow(
                animalsProfessionsTable,
                finallyDisplayLines,
                kombiTable_Kombis,
                maintable2subtable_Relation,
                newTable,
                old2newTable,
                paramLines,
                "kombi.csv",
            )

        if len(self.rowsOfcombi2) > 0:
            newTable = self.combiTableWorkflow(
                animalsProfessionsTable2,
                finallyDisplayLines,
                kombiTable_Kombis2,
                maintable2subtable_Relation2,
                newTable,
                old2newTable,
                paramLines,
                "kombi-meta.csv",
            )

        newTable = self.tables.getOut.onlyThatColumns(
            newTable, spaltenreihenfolgeundnurdiese
        )

        self.tables.getOut.cliOut(finallyDisplayLines, newTable, numlen, rowsRange)

    def combiTableWorkflow(
        self,
        animalsProfessionsTable,
        finallyDisplayLines,
        kombiTable_Kombis,
        maintable2subtable_Relation,
        newTable,
        old2newTable,
        paramLines,
        csvFileName,
    ):
        """alle  Schritte für kombi:
        1. lesen: KombiTable und relation, was von kombitable zu haupt gehört
                  und matrix mit zellen sind zahlen der kombinationen
                  d.h. 3 Sachen sind das Ergebnis
        2. prepare: die Zeilen, die infrage kommen für Kombi, d.h.:
                                key = haupttabellenzeilennummer
                                value = kombitabellenzeilennummer
        3. Zeilenumbruch machen, wie es bei der Haupt+Anzeige-Tabelle auch gemacht wurde
           prepare4out
        4. Vorbereiten des Joinens beider Tabellen direkt hier rein programmiert
           (Müsste ich unbedingt mal refactoren!)
        5. joinen
           Wenn ich hier jetzt alles joine, und aber nicht mehrere Zellen mache pro Kombitablezeile,
           d.h. nicht genauso viele Zeilen wie es der Kombitablezeilen entspricht,
           d.h. ich mache nur eine Zeile, in der ich alle kombitableteilen nur konkatteniere,
           dann ist das Ergebnis Mist in der Ausagbe, weil der Zeilenumbruch noch mal gemacht werden müsste,
           der jedoch bereits schon gemacht wurde.
           Der musste aber vorher gemacht werden, denn wenn man ihn jetzt machen würde,
           dann müsste man das eigentlich WIEDER mit der ganzen Tabelle tun!
           Also etwa alles völlig umprogrammieren?
        6. noch mal nur das ausgeben lassen, das nur ausgegeben werden soll
        7. letztendliche Ausagebe von allem!!
        """
        ChosenKombiLines = self.tables.getCombis.prepare_kombi(
            finallyDisplayLines,
            animalsProfessionsTable,
            paramLines,
            finallyDisplayLines,
            kombiTable_Kombis,
        )
        komb_rows = (
            self.rowsOfcombi
            if csvFileName == "kombi.csv"
            else (self.rowsOfcombi2 if csvFileName == "kombi-meta.csv" else None)
        )
        (
            finallyDisplayLines_kombi,
            newTable_kombi_1,
            lineLen_kombi_1,
            animalsProfessionsTable,
            old2newTableAnimalsProfessions,
        ) = self.tables.getPrepare.prepare4out(
            OrderedSet(),
            OrderedSet(),
            animalsProfessionsTable,
            komb_rows,
            self.tables.getCombis.sumOfAllCombiRowsAmount,
            reliTableLenUntilNow=len(newTable[0])
            - (
                len(self.rowsOfcombi) + len(self.rowsOfcombi2)
                if csvFileName == "kombi.csv"
                else len(self.rowsOfcombi2)
                if csvFileName == "kombi-meta.csv"
                else None
            ),
            kombiCSVNumber=0
            if csvFileName == "kombi.csv"
            else 1
            if csvFileName == "kombi-meta.csv"
            else None,
        )
        KombiTables = self.tables.getCombis.prepareTableJoin(
            ChosenKombiLines, newTable_kombi_1
        )
        newTable = self.tables.getCombis.tableJoin(
            newTable,
            KombiTables,
            maintable2subtable_Relation,
            old2newTable,
            komb_rows,
        )
        return newTable


if __name__ == "__main__":
    # try:
    Program(sys.argv)
    # except KeyboardInterrupt:
    #    sys.exit()
