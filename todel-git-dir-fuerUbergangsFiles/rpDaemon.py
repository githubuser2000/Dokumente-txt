#!/usr/bin/env pypye
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))
import os
import platform
import pprint
import re
import subprocess
from collections import OrderedDict, defaultdict
from copy import copy, deepcopy
from enum import Enum
from fractions import Fraction
from itertools import zip_longest
from typing import Optional

from center import (
    alxp,
    cliout,
    i18n,
    invert_dict_B,
    isZeilenAngabe,
    isZeilenAngabe_betweenKommas,
    isZeilenBruchAngabe,
    kpattern,
    moduloA,
    primfaktoren,
    primRepeat,
    retaPromptHilfe,
    teiler,
    textHatZiffer,
    x,
    multiples,
)
from LibRetaPrompt import (
    BereichToNumbers2,
    PromptModus,
    gebrochenErlaubteZahlen,
    isReTaParameter,
    notParameterValues,
    stextFromKleinKleinKleinBefehl,
    verifyBruchNganzZahlBetweenCommas,
    verkuerze_dict,
    wahl15,
    wahl16,
    custom_split,
    custom_split2,
)

# import reta
from nestedAlx import (
    ComplSitua,
    NestedCompleter,
    ausgabeParas,
    befehle,
    befehle2,
    hauptForNeben,
    kombiMainParas,
    mainParas,
    reta,
    retaProgram,
    spalten,
    spaltenDict,
    zeilenParas,
)
from prompt_toolkit import PromptSession, print_formatted_text, prompt

# from prompt_toolkit.completion import Completer, Completion, WordCompleter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.styles import Style
from word_completerAlx import WordCompleter

from multis import mult2
from multis3 import mult3

i18nRP = i18n.retaPrompt
wahl15[""] = wahl15["15"]
wahl16[""] = wahl16["16"]
befehle += ["15_"]
befehle += ["16_"]
befehleBeenden = i18nRP.befehleBeenden
# befehleBeenden = {"ende", "exit", "quit", "q", ":q"}
infoLog = False
sprachenWahl = "deutsch"


class TXT(object):
    _text = ""
    _platzhalter = ""
    _stext = []
    _stextS = []
    _stextE = []
    _e = []
    _stextEmenge = set()
    _stextSet = set()
    _befehlDavor = ""

    def hasWithoutABC(self, hasSet: set) -> bool:
        """tells if any values of given set exists in TXT.menge and command abc and abcd is not inside"""
        return (
            len(hasSet & self._stextSet) > 0
            and len({i18n.befehle2["abc"], i18n.befehle2["abcd"]} & self._stextSet) == 0
        )

    def has(self, hasSet: set) -> bool:
        """tells if any values of given set exists in TXT.menge"""
        return len(hasSet & self._stextSet) > 0

    def __init__(self, txt=""):
        self.text = txt.strip()

    @property
    def e(self):
        return self._e

    @property
    def menge(self):
        return self._stextSet

    @property
    def listeE(self):
        return self._stextE

    @property
    def listeS(self):
        return self._stextS

    @property
    def liste(self):
        return self._stext

    @property
    def mengeE(self):
        return self._stextEmenge

    @property
    def platzhalter(self):
        return self._platzhalter

    @property
    def text(self):
        return self._text

    @platzhalter.setter
    def platzhalter(self, value):
        self._platzhalter = value.strip()

    @text.setter
    def text(self, value):
        assert type(value) is str
        value = str(value).strip()
        self._text = value
        if value[:4] != "reta":
            self._stext = custom_split(self._text)
            self._stextS = custom_split(self._text)
        else:
            self._stext = [s.strip() for s in self._text.split() if len(s.strip()) > 0]
            self._stextS = value.split()
        self._stextSet = set(self._stext)
        self._stextEmenge = self._stextSet | set(self._e)
        self._stextE = self._stext + self._e

    @liste.setter
    def liste(self, value):
        assert type(value) is list
        self._stext = [s.strip() for s in value if len(s.strip()) > 0]
        self._stextSet = set(self._stext)
        self._stextEmenge = self._stextSet | set(self._e)
        self._stextE = self._stext + self._e
        self._stextS = [s for g in [custom_split(v) for v in value] for s in g]

    @e.setter
    def e(self, value):
        assert type(value) is list
        self._e = value
        self._stextEmenge = self._stextSet | set(self._e)
        self._stextE = self._stext + self._e

    @property
    def befehlDavor(self):
        return self._befehlDavor

    @befehlDavor.setter
    def befehlDavor(self, value):
        self._befehlDavor = value


def anotherOberesMaximum(zahlenBereichC, maxNum, Txt):
    maximizing = list(BereichToNumbers2(zahlenBereichC, False, 0))
    if len(maximizing) > 0:
        maximizing.sort()
        maxNum2 = maximizing[-1]
    else:
        maxNum2 = maxNum
    try:
        max1024 = Txt.programm.tables.hoechsteZeile[1024]
    except Exception:
        max1024 = retaProgram.tables.hoechsteZeile[1024]
    return (
        "--"
        + i18n.zeilenParas["oberesmaximum"]
        + "="
        + str(max(maxNum, maxNum2, max1024) + 1)
    )


def newSession(history=False):
    class ToggleHistory(FileHistory):
        def __init__(self, file_path, *args, **kwargs):
            super().__init__(file_path, *args, **kwargs)
            self.inner_history = FileHistory(file_path)
            self.logging_enabled = True

        def append_string(self, string):
            if (
                self.logging_enabled
                and i18n.befehle2["nichtloggen"] not in custom_split(string)
                and i18n.befehle2["loggen"] not in custom_split(string)
            ):
                super().append_string(string)

        def get_strings(self):
            return self.inner_history.get_strings()

        def enable_logging(self):
            self.logging_enabled = True

        def disable_logging(self):
            self.logging_enabled = False

        def add_to_history(self, string):
            self.append_string(string)

    if history:
        return PromptSession(
            # history=FileHistory(os.path.expanduser("~") + os.sep + ".ReTaPromptHistory")
            history=ToggleHistory(
                os.path.expanduser("~") + os.sep + ".ReTaPromptHistory"
            )
        )
    else:
        return PromptSession()


def returnOnlyParasAsList(textList: str):
    liste = []
    for t in textList:
        if isReTaParameter(t):
            liste += [t]
    return liste


# def externCommand(cmd: str, StrNummern: str):
#    nummern: list = list(BereichToNumbers2(StrNummern, False, 0))
#    nummern.sort()
#    nummernStr: list = [str(nummer) for nummer in nummern]
#    try:
#        process = subprocess.Popen(
#            [os.path.dirname(__file__) + os.sep + cmd, *nummernStr]
#        )
#        process.wait()
#    except:
#        pass
#


def grKl(A: set, B: set) -> tuple:
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
    if type(text) is not str:
        return []
    bruchSpalten: list = text.split("/")
    bruchSpaltenNeu = []
    bruchSpaltenNeu2 = []
    if len(bruchSpalten) < 2:
        """Ein Bruch hat immer mindestens 2 Zahlen"""
        return []
    keineZahl = OrderedDict()
    for k, bS in enumerate(bruchSpalten):
        keineZahlBefore = keineZahl
        zahl, keineZahl, bsNeu = OrderedDict(), OrderedDict(), []
        countChar = 0
        countNumber = 0
        wasNumber = False
        goNext = 0
        for char in bS:
            if char.isdecimal():
                """alles was Zahlen sind"""
                if not wasNumber:
                    goNext += 1
                try:
                    zahl[goNext] += char
                except KeyError:
                    zahl[goNext] = char
                wasNumber = True
                countNumber += 1
                countChar = 0
            else:
                """alles was keine Zahlen sind"""
                if wasNumber:
                    goNext += 1
                try:
                    keineZahl[goNext] += char
                except KeyError:
                    keineZahl[goNext] = char
                wasNumber = False
                countChar += 1
                countNumber = 0
        flag: bool = False
        allVergleich: list[bool] = [
            zahl2 > zahl1 for zahl1, zahl2 in zip(keineZahl.keys(), zahl.keys())
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


def createRangesForBruchLists(bruchList: list) -> tuple:
    n1, n2 = [], []
    listenRange: range = range(0)
    listenRangeUrsprung: range = range(0)
    flag = 0
    # ergebnis: list[tuple[range | str]] = []
    ergebnis = []
    if (
        len(bruchList) == 3
        and len(bruchList[0]) == 0
        and len(bruchList[1]) == 2
        and len(bruchList[2]) == 0
        and (bruchList[1][0] + bruchList[1][1]).isdecimal()
    ):
        return [int(bruchList[1][0])], bruchList[1][1]
    for i, b in enumerate(bruchList):
        if flag == -1:
            return []
        if flag > 3:
            """illegal"""
            return []
        elif flag == 3:
            """Es war ein Bruch"""
            ergebnis += [str(n2[-2]), "-", str(n2[-1])]

            listenRange = range(int(n1[-2]), int(n1[-1]) + 1)
            listenRangeUrsprung = listenRange
            flag = -1
        if len(b) == 2 and (b[0] + b[1]).isdecimal():
            """Es ist ein Bruch"""
            if (
                len(bruchList) >= i
                and len(bruchList[i + 1]) == 1
                and bruchList[i + 1][0] == "-"
                and flag == 0
            ) or (
                i > 0
                and len(bruchList[i - 1]) == 1
                and bruchList[i - 1][0] == "-"
                and flag == 2
            ):
                n1 += [int(b[0])]
                n2 += [int(b[1])]
                flag += 1
            else:
                ergebnis += [b[1]]
                if (
                    len(listenRange) > 0
                    and i > 0
                    and len(bruchList[i - 1]) == 1
                    and bruchList[i - 1][0] == "+"
                ):
                    listenRange2 = []
                    for lr in listenRangeUrsprung:
                        listenRange2 += [lr + int(b[0]), lr - int(b[0])]
                    listenRange = listenRange2
                elif len(listenRange) == 0:
                    listenRange = [int(b[0])]
                    listenRangeUrsprung = listenRange
        elif len(b) == 1 and b[0] == "-" and flag > 0:
            flag += 1

        else:
            """Es ist kein Bruch"""
            flag = 0
            ergebnis += [*b]
    ergebnis2 = "".join(ergebnis)
    return listenRange, ergebnis2


def speichern(ketten, platzhalter, text):
    global promptMode2, textDazu0
    bedingung1 = len(platzhalter) > 0
    bedingung2 = len(ketten) > 0
    Txt = TXT(text)
    Txt.platzhalter = platzhalter
    if bedingung1 or bedingung2:
        if bedingung1:
            woRetaBefehl = []
            TxtPlatzhalter = TXT(Txt.platzhalter)
            if Txt.liste[:1] == ["reta"]:
                woRetaBefehl += ["bereits-dabei"]
                Txt.liste.pop(0)
            if TxtPlatzhalter.liste[:1] == ["reta"]:
                woRetaBefehl += ["bei-dazu"]
                TxtPlatzhalter.liste.pop(0)
            if len(woRetaBefehl) > 0:
                Txt.platzhalter = (
                    "reta " + " ".join(TxtPlatzhalter.liste) + " " + " ".join(Txt.liste)
                )
            else:  # erstes und zweites heißt nicht reta am Anfang
                # nochmal für nicht Kurzbefehle befehle, also ohne "reta" am Anfang
                textUndPlatzHalterNeu = []
                langKurzBefehle = []
                for rpBefehl in custom_split(Txt.platzhalter) + Txt.liste:
                    if rpBefehl in befehle and len(rpBefehl) > 1:
                        langKurzBefehle += [rpBefehl.strip()]
                    else:  # Kurzbefehl oder irgendwas anderes
                        textUndPlatzHalterNeu += [rpBefehl.strip()]
                rpBefehlE = ""
                for rpBefehl in textUndPlatzHalterNeu:
                    rpBefehlSplitted = custom_split(str(rpBefehl))
                    if len(rpBefehlSplitted) > 0:
                        rpBefehlE += " ".join(rpBefehlSplitted) + " "
                rpBefehlE = rpBefehlE[:-1]
                Txt2 = TXT()
                Txt2.liste = textUndPlatzHalterNeu
                ifKurzKurz, Txt2.liste = stextFromKleinKleinKleinBefehl(
                    PromptModus.AusgabeSelektiv, Txt2.liste, []
                )
                replacements = i18nRP.replacements
                if len(textUndPlatzHalterNeu) > 0 and Txt2.liste[0] not in [
                    "reta",
                    i18n.befehle2["shell"],
                    i18n.befehle2["python"],
                    i18n.befehle2["abstand"],
                ]:
                    listeNeu: list = []
                    for token in Txt2.liste:
                        try:
                            listeNeu += [replacements[token]]
                        except KeyError:
                            listeNeu += [token]
                    Txt2.liste = listeNeu

                Txt.platzhalter = " ".join(Txt2.liste + langKurzBefehle)
    else:
        Txt.platzhalter = "" if Txt.text is None else str(Txt.text)
    Txt.text = ""
    if Txt.platzhalter != "" or not (bedingung1 or bedingung2):
        promptMode2 = PromptModus.AusgabeSelektiv
    else:
        promptMode2 = PromptModus.normal
    (
        bedingungX,
        bruecheX,
        cX,
        ketten2X,
        maxNum2X,
        stextX,
        zahlenAngaben_X,
        ifKurzKurz_X,
    ) = promptVorbereitungGrosseAusgabe(
        Txt.platzhalter,
        promptMode2,
        promptMode2,
        PromptModus.normal,
        Txt.platzhalter,
        [],
    )

    # textDazu0 = platzhalter.split()
    textDazu0 = stextX
    return ketten, Txt


def PromptScope():
    global promptMode2, textDazu0
    (
        befehleBeenden,
        loggingSwitch,
        promptDavorDict,
        promptMode,
        startpunkt1,
        nurEinBefehl,
        immerEbefehlJa,
    ) = PromptAllesVorGroesserSchleife()
    global textDazu0, sprachenWahl
    Txt = TXT("")
    nochAusageben = ""
    ketten = []
    while len(Txt.menge & befehleBeenden) == 0 or Txt.has(
        {i18n.befehle2["abc"], i18n.befehle2["abcd"]}
    ):
        cmd_gave_output = False
        promptModeLast = promptMode

        if promptMode not in (
            PromptModus.speicherungAusgaben,
            PromptModus.speicherungAusgabenMitZusatz,
        ):
            Txt = promptInput(
                loggingSwitch,
                promptDavorDict,
                promptMode,
                startpunkt1,
                Txt,
                nurEinBefehl,
                immerEbefehlJa,
            )
            ketten, Txt = promptSpeicherungA(ketten, promptMode, Txt)

        else:
            Txt = promptSpeicherungB(nochAusageben, promptMode, Txt)
            # textE = []

        if promptMode == PromptModus.loeschenSelect:
            Txt.text, promptMode, _ = PromptLoescheVorSpeicherungBefehle(
                Txt.platzhalter, promptMode, Txt.text
            )
            Txt.platzhalter = Txt.text
            textDazu0 = Txt.liste
            continue

        promptMode = PromptModus.normal

        if (
            (
                Txt.hasWithoutABC(
                    {i18n.befehle2["S"], i18n.befehle2["BefehlSpeichernDanach"]}
                )
            )
        ) and len(Txt.liste) == 1:
            promptMode = PromptModus.speichern
            continue
        elif (
            (
                Txt.hasWithoutABC(
                    {i18n.befehle2["s"], i18n.befehle2["BefehlSpeichernDavor"]}
                )
            )
        ) and len(Txt.liste) == 1:
            ketten, Txt = speichern(ketten, Txt.platzhalter, Txt.befehlDavor)
            promptMode = PromptModus.normal
            continue
        elif (
            len(
                Txt.menge
                - {
                    i18n.befehle2["s"],
                    i18n.befehle2["BefehlSpeichernDavor"],
                    i18n.befehle2["S"],
                    i18n.befehle2["BefehlSpeichernDanach"],
                }
            )
            > 0
            and (
                len(
                    Txt.menge
                    & {
                        i18n.befehle2["s"],
                        i18n.befehle2["BefehlSpeichernDavor"],
                        i18n.befehle2["S"],
                        i18n.befehle2["BefehlSpeichernDanach"],
                    }
                )
                == 1
            )
            and not Txt.has({i18n.befehle2["abc"], i18n.befehle2["abcd"]})
        ):
            stextB = copy(Txt.liste)
            for val in (
                i18n.befehle2["s"],
                i18n.befehle2["S"],
                i18n.befehle2["BefehlSpeichernDavor"],
                i18n.befehle2["BefehlSpeichernDanach"],
            ):
                try:
                    stextB.remove(val)
                except ValueError:
                    pass
            ketten, Txt = speichern(ketten, Txt.platzhalter, " ".join(stextB))
            Txt.liste = []
            Txt.text = ""
            Txt.befehlDavor = ""
            promptMode = PromptModus.normal
            continue
        elif (
            (
                Txt.hasWithoutABC(
                    {i18n.befehle2["o"], i18n.befehle2["BefehlSpeicherungAusgeben"]}
                )
            )
        ) and len(Txt.liste) == 1:
            promptMode = PromptModus.speicherungAusgaben
            continue
        elif (
            Txt.hasWithoutABC(
                {i18n.befehle2["o"], i18n.befehle2["BefehlSpeicherungAusgeben"]}
            )
        ) and len(
            Txt.menge - {i18n.befehle2["o"], i18n.befehle2["BefehlSpeicherungAusgeben"]}
        ) > 1:
            nochAusageben = Txt.liste
            promptMode = PromptModus.speicherungAusgabenMitZusatz
            continue
        elif (
            (
                Txt.hasWithoutABC(
                    {i18n.befehle2["l"], i18n.befehle2["BefehlSpeicherungLöschen"]}
                )
            )
        ) and len(Txt.liste) == 1:
            if "--" + i18n.ausgabeParas["nocolor"] in Txt.listeE:
                print(
                    str(
                        [
                            {i + 1, a}
                            for i, a in enumerate(custom_split(Txt.platzhalter))
                        ]
                    )
                )
            else:
                cliout(
                    str(
                        [
                            {i + 1, a}
                            for i, a in enumerate(custom_split(Txt.platzhalter))
                        ]
                    ),
                    True,
                )
                promptMode = PromptModus.loeschenSelect
                continue

        text1, text2, text3 = verdreheWoReTaBefehl(
            Txt.platzhalter, Txt.text, textDazu0, promptMode
        )

        (
            IsPureOnlyReTaCmd,
            brueche,
            zahlenBereichC,
            ketten,
            maxNum,
            Txt.liste,
            zahlenAngaben_,
            ifKurzKurz,
        ) = promptVorbereitungGrosseAusgabe(
            text1,
            promptMode,
            promptMode2,
            promptModeLast,
            text2,
            text3,
        )
        loggingSwitch = PromptGrosseAusgabe(
            IsPureOnlyReTaCmd,
            befehleBeenden,
            brueche,
            zahlenBereichC,
            ketten,
            loggingSwitch,
            maxNum,
            cmd_gave_output,
            zahlenAngaben_,
            ifKurzKurz,
            nurEinBefehl,
            Txt,
        )


def vorherVonAusschnittOderZaehlung(Txt: TXT, bereichsAngabe: str) -> str:
    if Txt.hasWithoutABC({i18n.befehle2["range"], i18n.befehle2["R"]}):
        return "".join(("--", i18n.zeilenParas["zaehlung"], "=", bereichsAngabe))
    else:
        return "".join(
            (("--", i18n.zeilenParas["vorhervonausschnitt"], "=", bereichsAngabe))
        )


def PromptGrosseAusgabe(
    IsPureOnlyReTaCmd,
    befehleBeenden,
    brueche,
    zahlenBereichC,
    ketten,
    loggingSwitch,
    maxNum,
    cmd_gave_output,
    zahlenAngaben_,
    ifKurzKurz,
    nurEinBefehl,
    Txt,
):
    # global alxp, cliout, i18n, invert_dict_B, isZeilenAngabe, isZeilenAngabe_betweenKommas, isZeilenBruchAngabe, moduloA, primfaktoren, primRepeat, retaPromptHilfe, teiler, textHatZiffer, x
    global i18nRP, sprachenWahl

    (
        EsGabzahlenAngaben,
        zahlenReiheKeineWteiler,
        bruch_GanzZahlReziproke,
        fullBlockIsZahlenbereichAndBruch,
        rangesBruecheDict,
        rangesBruecheDictReverse,
    ) = (False, "", [], False, {}, {})
    if not IsPureOnlyReTaCmd:
        (
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            zahlenReiheKeineWteiler,
            fullBlockIsZahlenbereichAndBruch,
            rangesBruecheDict,
            EsGabzahlenAngaben,
            rangesBruecheDictReverse,
            Txt.liste,
        ) = bruchBereichsManagementAndWbefehl(zahlenBereichC, Txt.liste, zahlenAngaben_)
    if Txt.hasWithoutABC({i18n.befehle2["mulpri"], i18n.befehle2["p"]}):
        Txt.liste += [
            i18n.befehle2["multis"],
            i18n.befehle2["prim"],
            i18n.befehle2["primfaktorenvergleich"],
        ]

    if ifPrintCmdAgain(Txt):
        if "--" + i18n.ausgabeParas["nocolor"] in Txt.listeE:
            print("[code]" + Txt.text + "[/code]")
        else:
            cliout("[code]" + Txt.text + "[/code]", True, i18n.ausgabeArt["bbcode"])
    if (
        ifKurzKurz
        and i18n.befehle2["keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"]
        not in Txt.listeE
    ):
        if ifPrintCmdAgain(Txt):
            if "--" + i18n.ausgabeParas["nocolor"] in Txt.listeE:
                print(
                    i18nRP.promptModeSatz2.format(
                        "[code]", " ".join(Txt.listeE), "[/code]", Txt.text
                    )
                )
            else:
                cliout(
                    i18nRP.promptModeSatz2.format(
                        "[code]", " ".join(Txt.listeE), "[/code]", Txt.text
                    ),
                    True,
                    "",
                )
        else:
            if "--" + i18n.ausgabeParas["nocolor"] in Txt.listeE:
                print(
                    i18nRP.promptModeSatz2.format(
                        "'", " ".join(Txt.listeE), "'", Txt.text
                    )
                )
            else:
                cliout(
                    i18nRP.promptModeSatz2.format(
                        "'", " ".join(Txt.listeE), "'", Txt.text
                    ),
                    True,
                    "",
                )
    if Txt.has({i18n.befehle2["abcd"], i18n.befehle2["abc"]}):
        buchstabe: str
        # befehlskette = list(
        #    set(Txt.text.split()) - {i18n.befehle2["multis"], i18n.befehle2["prim"]}
        # )
        befehlskette = Txt.text.split()
        if (
            len(befehlskette)
            == 2
            # and len(befehlskette[0]) > 1
            # and len(befehlskette[1]) > 1
        ):
            cmd_gave_output = True
            if True or befehlskette[1] not in i18nRP.replacements.values():
                if (
                    befehlskette[0] == i18n.befehle2["abc"]
                    or befehlskette[0] == i18n.befehle2["abcd"]
                ):
                    buchstaben = befehlskette[1]
                else:
                    buchstaben = befehlskette[0]
            else:
                if (
                    befehlskette[0] == i18n.befehle2["abc"]
                    or befehlskette[0] == i18n.befehle2["abcd"]
                ):
                    buchstaben = {
                        value: key for key, value in i18nRP.replacements.items()
                    }[befehlskette[1]]
                else:
                    buchstaben = {
                        value: key for key, value in i18nRP.replacements.items()
                    }[befehlskette[0]]
            print(
                str(
                    " ".join(
                        [
                            "".join(str(ord(buchstabe.lower()) - 96))
                            for buchstabe in buchstaben
                        ]
                    )
                )
            )
    if Txt.hasWithoutABC({i18n.befehle2["kurzbefehle"]}):
        cmd_gave_output = True
        print(
            "{}: {}\n{}".format(
                i18nRP.befehleWort["Kurzbefehle"],
                " ".join([b for b in befehle if len(b) == 1]),
                str(i18nRP.replacements),
            )
        )

    if Txt.hasWithoutABC({i18n.befehle2["befehle"]}):
        cmd_gave_output = True
        print("{}: {}".format(i18nRP.befehleWort["Befehle"], str(befehle)[1:-1]))
    if Txt.hasWithoutABC(
        {i18n.befehle2["h"], i18n.befehle2["help"], i18n.befehle2["hilfe"]}
    ):
        cmd_gave_output = True
        retaPromptHilfe()
    bedingungZahl, bedingungBrueche = (
        EsGabzahlenAngaben,
        (len(bruch_GanzZahlReziproke) > 0 or len(rangesBruecheDict) > 0)
        or len(rangesBruecheDictReverse) > 0,
    )
    if IsPureOnlyReTaCmd:
        cmd_gave_output = True
        import reta

        if (
            i18n.befehle2["keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"]
            not in Txt.listeE
            and not ifKurzKurz
        ):
            if not ifPrintCmdAgain(Txt):
                # weil sonst das doppelt gemacht wird
                cliout(" ".join(Txt.liste), True, "")

        Txt.liste2 = " ".join(Txt.liste)
        Txt.liste3 = Txt.liste2.split(" -")
        Txt.liste4 = Txt.liste3[:1] + ["-" + a for a in Txt.liste3[1:]]
        Txt.programm = reta.Program(Txt.liste4)

    zeiln1, zeiln2, zeiln3, zeiln4 = zeiln1234create(
        Txt,
        bedingungZahl,
        bruch_GanzZahlReziproke,
        zahlenBereichC,
        maxNum,
        zahlenReiheKeineWteiler,
    )

    if bedingungZahl:
        if Txt.hasWithoutABC({i18n.befehle2["thomas"], i18n.befehle2["t"]}):
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                [
                    "".join(
                        ("--", i18n.ParametersMain.galaxie[0], "=", i18n.thomasWort)
                    ),
                ],
                "2",
                Txt,
            )

    if (
        False
        and {"english", "englisch"} & Txt.menge != set()
        and sys.argv[0].split(os.sep)[-1] == "rpl"
    ):
        cmd_gave_output = True
        sprachenWahl = "english"
        print("set to english")
        return loggingSwitch
        from importlib import reload

        import __main__
        import center
        import lib4tables
        import lib4tables_concat
        import lib4tables_Enum
        import lib4tables_prepare
        import LibRetaPrompt
        import nestedAlx
        import prompt_toolkit
        import prompt_toolkit.completion
        import prompt_toolkit.history
        import prompt_toolkit.styles
        import tableHandling
        import word_completerAlx

        import reta
        import retaPrompt

        for a in range(2):
            reload(center)
            reload(i18n)
            reload(LibRetaPrompt)
            reload(tableHandling)
            reload(reta)
            reload(nestedAlx)
            reload(word_completerAlx)
            reload(tableHandling)
            reload(lib4tables_Enum)
            reload(lib4tables_prepare)
            reload(lib4tables)
            reload(lib4tables_concat)
            reload(prompt_toolkit)
            reload(prompt_toolkit.completion)
            reload(prompt_toolkit.history)
            reload(prompt_toolkit.styles)
            reload(retaPrompt)
            i18nRP = i18n.retaPrompt

    if fullBlockIsZahlenbereichAndBruch and (bedingungZahl or bedingungBrueche):
        if Txt.hasWithoutABC({i18n.befehle2["leeren"]}):
            for _ in range(os.get_terminal_size().lines + 1):
                print()
            cmd_gave_output = True

        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["emotion"], i18n.befehle2["E"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        i18n.emotionWort,
                    )
                )
            ],
            None,
            ("2,3", "4,5"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        if was_n_1proN_cmd:
            nennerZaehlerGleich = []
            if len(rangesBruecheDict) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDict.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochenemotion"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "2",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )

            elif len(rangesBruecheDictReverse) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDictReverse.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochenemotion"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "1",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )

        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["W"], i18n.befehle2["wirklichkeit"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        wahl15["10"],
                    )
                )
            ],
            None,
            ("1,2", "5"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )

        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["T"], i18n.befehle2["triebe"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        wahl15["6"],
                    )
                )
            ],
            None,
            ("1", "2"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["I"], i18n.befehle2["impulse"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        wahl15["5"],
                    )
                )
            ],
            None,
            ("1,4", "3"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["B"], i18n.befehle2["bewusstsein"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        wahl15["15"],
                    )
                )
            ],
            None,
            ("6", "7"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["geist"], i18n.befehle2["G"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.grundstrukturen[0],
                        "=",
                        i18n.geistWort,
                    )
                )
            ],
            None,
            ("3", "4"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["freiheit"], i18n.befehle2["gleichheit"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.planet[0],
                        "=",
                        i18n.befehle2["freiheit"],
                    )
                )
            ],
            None,
            ("1-4,8", "5-7"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["groesse"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.strukturgroesse[0],
                        "=",
                        i18n.organisationWort,
                    )
                )
            ],
            None,
            ("1-3", "99"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["groesse"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.strukturgroesse[0],
                        "=",
                        i18n.ParametersMain.strukturgroesse[0],
                    )
                )
            ],
            None,
            ("1,2", "4"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        if was_n_1proN_cmd:
            nennerZaehlerGleich = []
            if len(rangesBruecheDict) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDict.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochengroesse"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "2",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )

            elif len(rangesBruecheDictReverse) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDictReverse.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochengroesse"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "1",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )

        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["kugeln"],
                    i18n.befehle2["kreise"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.universum[0],
                        "=",
                        i18n.kugelnKreise[0],
                    )
                )
            ],
            None,
            ("1-2", "99"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["netzwerk"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.universum[0],
                        "=",
                        i18n.netzwerkWort,
                    )
                )
            ],
            None,
            ("1-3", "99"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["komplex"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.universum[0],
                        "=",
                        i18n.komplexWort,
                    )
                )
            ],
            None,
            ("1", "3"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC(
                {
                    i18n.befehle2["absicht"],
                    i18n.befehle2["absichten"],
                    i18n.befehle2["motiv"],
                    i18n.befehle2["motive"],
                    i18n.befehle2["a"],
                }
            ),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.menschliches[0],
                        "=",
                        i18n.motivationWort,
                    )
                )
            ],
            None,
            ("1", "3"),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        if was_n_1proN_cmd:
            if len(rangesBruecheDict) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDict.items():
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, ",".join(zaehler)),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochengalaxie"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "2",
                        Txt,
                    )
            elif len(rangesBruecheDictReverse) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDictReverse.items():
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, ",".join(zaehler)),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochengalaxie"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "1",
                        Txt,
                    )

        eigN, eigR = [], []
        for aa in Txt.listeE:
            if i18n.EIGS_N_R[0] == aa[: len(i18n.EIGS_N_R[0])]:
                eigN += [aa[len(i18n.EIGS_N_R[0]) :]]
            if i18n.EIGS_N_R[1] == aa[: len(i18n.EIGS_N_R[1])]:
                eigR += [aa[len(i18n.EIGS_N_R[0]) :]]

        if len(eigN) > 0:
            if len(zahlenBereichC) > 0:
                cmd_gave_output = True
                retaExecuteNprint(
                    ketten,
                    Txt.listeE,
                    zeiln1,
                    zeiln2,
                    ["".join(("--", i18n.konzeptE["konzept"], "=", (",".join(eigN))))],
                    None,
                    Txt,
                )

        if len(eigR) > 0:
            cmd_gave_output = True
            # zeilenAusReziprokenDazu = ",".join(
            #    [
            #        bruch.split("/")[0]
            #        for bruch in bruch_GanzZahlReziproke.split(",")
            #        if bruch.split("/")[0] != ""
            #    ]
            # )

            # if len(zeiln1) > 1 and i18n.zeilenParas["oberesmaximum"] not in zeiln1:
            #    zeiln1 += (
            #        "," if zeiln1[-1].isdecimal() else ""
            #    ) + zeilenAusReziprokenDazu
            # if len(zeiln2) > 1 and i18n.zeilenParas["oberesmaximum"] not in zeiln2:
            #    zeiln2 += (
            #        "," if zeiln2[-1].isdecimal() else ""
            #    ) + zeilenAusReziprokenDazu
            ZahlenAngabenCneu = zahlenBereichC + "," + bruch_GanzZahlReziproke
            ZahlenAngabenCneu = ZahlenAngabenCneu.replace(",,", ",")
            ZahlenAngabenCneu = ZahlenAngabenCneu.strip(",")

            TxtNeu = deepcopy(Txt)
            TxtNeu.text += " " + bruch_GanzZahlReziproke
            # zeiln1Neu, zeiln2Neu, _, _ = zeiln1234create(
            #    TxtNeu,
            #    lenbruch_GanzZahlReziproke > 0,
            #    "",
            #    cNeu,
            #    maxNum,
            #    zahlenReiheKeineWteiler
            #    + ("," if len(zahlenReiheKeineWteiler) > 0 else "")
            #    + bruch_GanzZahlReziproke,
            # )
            # x(
            #    "EIGR",
            #    (
            #        cNeu,
            #        ketten,
            #        Txt.listeE,
            #        " ".join((zeiln3, zeiln1)),
            #        " ".join((zeiln4, zeiln2)),
            #        zahlenReiheKeineWteiler,
            #    ),
            # )
            if len(ZahlenAngabenCneu) > 0:
                retaExecuteNprint(
                    ketten + ["-" + i18n.hauptForNeben["zeilen"], zeiln1, zeiln2],
                    Txt.listeE,
                    zeiln3,
                    zeiln4,
                    ["".join(("--", i18n.konzeptE["konzept2"], "=", (",".join(eigR))))],
                    None,
                    Txt,
                )
            del ZahlenAngabenCneu
        was_n_1proN_cmd, cmd_gave_output = retaCmdAbstraction_n_and_1pron(
            Txt.hasWithoutABC({i18n.befehle2["universum"], i18n.befehle2["u"]}),
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.universum[0],
                        "=",
                        i18n.transzendentalienWort,
                    )
                )
            ],
            [
                "".join(
                    (
                        "--",
                        i18n.ParametersMain.universum[0],
                        "=",
                        i18n.transzendentaliereziprokeWort,
                    )
                )
            ],
            (
                "1"
                + (
                    ",4"
                    if len(Txt.menge & set(befehle)) <= 2
                    and not Txt.hasWithoutABC(
                        {
                            i18n.befehle2[
                                "keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"
                            ],
                            i18n.befehle2["e"],
                            i18n.befehle2["ee"],
                            "--" + i18n.ausgabeParas["keineueberschriften"],
                        }
                    )
                    else ""
                ),
                "1"
                + (
                    ",2"
                    if len(Txt.menge & set(befehle)) <= 2
                    and not Txt.hasWithoutABC(
                        {
                            i18n.befehle2[
                                "keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"
                            ],
                            i18n.befehle2["e"],
                            i18n.befehle2["ee"],
                            "--" + i18n.ausgabeParas["keineueberschriften"],
                        }
                    )
                    else ""
                ),
            ),
            Txt,
            bruch_GanzZahlReziproke,
            zahlenBereichC,
            ketten,
            cmd_gave_output,
            zeiln1,
            zeiln2,
            zeiln3,
            zeiln4,
        )
        if was_n_1proN_cmd:
            nennerZaehlerGleich = []
            # nennerZaehlerMakesWholeNum = []
            # nennerZaehlerMakesWholeNumReziproke = []
            if len(rangesBruecheDict) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDict.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochenuniversum"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "2",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )
                    # nennerZaehlerMakesWholeNumS = findNennerZaehlerMakesWholeNum(
                    #    hierBereich,
                    #    nenner,
                    #    nennerZaehlerMakesWholeNum,
                    #    nennerZaehlerMakesWholeNumReziproke,
                    # )
                    # nennerZaehlerMakesWholeNum += nennerZaehlerMakesWholeNumS[0]
                    # nennerZaehlerMakesWholeNumReziproke += nennerZaehlerMakesWholeNumS[
                    #    1
                    # ]

            elif len(rangesBruecheDictReverse) > 0:
                cmd_gave_output = True
                for nenner, zaehler in rangesBruecheDictReverse.items():
                    hierBereich = ",".join(zaehler)
                    retaExecuteNprint(
                        ketten,
                        Txt.listeE,
                        vorherVonAusschnittOderZaehlung(Txt, hierBereich),
                        "",
                        [
                            "".join(
                                (
                                    "--",
                                    i18n.gebrochenUniGal["gebrochenuniversum"][0],
                                    "=",
                                    str(nenner),
                                )
                            )
                        ],
                        "1",
                        Txt,
                    )
                    nennerZaehlerGleich += findEqualNennerZaehler(
                        hierBereich, nenner, nennerZaehlerGleich
                    )
                    # nennerZaehlerMakesWholeNumS = findNennerZaehlerMakesWholeNum(
                    #    nenner,
                    #    hierBereich,
                    #    nennerZaehlerMakesWholeNum,
                    #    nennerZaehlerMakesWholeNumReziproke,
                    # )
                    # nennerZaehlerMakesWholeNum += nennerZaehlerMakesWholeNumS[0]
                    # nennerZaehlerMakesWholeNumReziproke += nennerZaehlerMakesWholeNumS[
                    #    1
                    # ]
            if len(nennerZaehlerGleich) != 0:
                cmd_gave_output = True
                nennerZaehlerGleich = set(nennerZaehlerGleich)
                nennerZaehlerGleich = ",".join(nennerZaehlerGleich)
                retaExecuteNprint(
                    ketten,
                    Txt.listeE,
                    vorherVonAusschnittOderZaehlung(Txt, nennerZaehlerGleich),
                    "",
                    [
                        "".join(
                            (
                                "--",
                                i18n.ParametersMain.universum[0],
                                "=",
                                i18n.verhaeltnisgleicherzahlWort,
                            )
                        )
                    ],
                    "1",
                    Txt,
                )
#            if False and len(nennerZaehlerMakesWholeNum) != 0:
#                cmd_gave_output = True
#                nennerZaehlerMakesWholeNum = set(nennerZaehlerMakesWholeNum)
#                nennerZaehlerMakesWholeNum = ",".join(nennerZaehlerMakesWholeNum)
#                retaExecuteNprint(
#                    ketten,
#                    Txt.listeE,
#                    vorherVonAusschnittOderZaehlung(Txt, nennerZaehlerMakesWholeNum),
#                    "",
#                    [
#                        "".join(
#                            (
#                                "--",
#                                i18n.ParametersMain.universum[0],
#                                "=",
#                                i18n.transzendentalienWort,
#                            )
#                        )
#                    ],
#                    "4",
#                    Txt,
#                )
#            if False and len(nennerZaehlerMakesWholeNumReziproke) != 0:
#                cmd_gave_output = True
#                nennerZaehlerMakesWholeNumReziproke = set(
#                    nennerZaehlerMakesWholeNumReziproke
#                )
#                nennerZaehlerMakesWholeNumReziproke = ",".join(
#                    nennerZaehlerMakesWholeNumReziproke
#                )
#                retaExecuteNprint(
#                    ketten,
#                    Txt.listeE,
#                    vorherVonAusschnittOderZaehlung(
#                        Txt, nennerZaehlerMakesWholeNumReziproke
#                    ),
#                    "",
#                    [
#                        "".join(
#                            (
#                                "--",
#                                i18n.ParametersMain.universum[0],
#                                "=",
#                                i18n.transzendentaliereziprokeWort,
#                            )
#                        )
#                    ],
#                    "2",
#                    Txt,
#                )
    if bedingungZahl:
        if (
            len(
                {i18n.befehle2["prim24"], i18n.befehle2["primfaktorzerlegungModulo24"]}
                & Txt.mengeE
            )
            > 0
        ):
            cmd_gave_output = True

            for arg in BereichToNumbers2(zahlenReiheKeineWteiler):
                print(
                    str(arg)
                    + ": "
                    + str(primRepeat(primfaktoren(int(arg), True)))[1:-1]
                    .replace("'", "")
                    .replace(", ", " ")
                )

        if Txt.hasWithoutABC({i18n.befehle2["primfaktorenvergleich"]}):
            cmd_gave_output = True
            bereiche = {}
            for geschriebenerZahlenBereich in re.split(
                r"\s|,", zahlenReiheKeineWteiler
            ):
                zahlenBereichBerechnet = BereichToNumbers2(
                    geschriebenerZahlenBereich, False, 0
                )
                for zahlInZahlenBereich in zahlenBereichBerechnet:
                    primFaktoren = primfaktoren(zahlInZahlenBereich)
                    bereiche[zahlInZahlenBereich] = {
                        primZahl: primFaktoren.count(primZahl)
                        for primZahl in primFaktoren
                    }
            gemeinsamePrimzahlen = {}
            for i, (geschriebenerZahlenBereich, primMap) in enumerate(bereiche.items()):
                if i == 0:
                    gemeinsamePrimzahlen = set(primMap.keys())
                else:
                    gemeinsamePrimzahlen &= set(primMap.keys())
            primGemeinsameVorkommen = {}
            for gemeinsamePrimzahl in gemeinsamePrimzahlen:
                vorkommens = []
                for i, (geschriebenerZahlenBereich, primMap) in enumerate(
                    bereiche.items()
                ):
                    vorkommens += [primMap[gemeinsamePrimzahl]]
                primGemeinsameVorkommen[gemeinsamePrimzahl] = min(vorkommens)
            gemeinsamePrimzahlenMatrix = [
                [primzahl] * vorkommenAnzahl
                for primzahl, vorkommenAnzahl in primGemeinsameVorkommen.items()
            ]
            gemeinsamePrimzahlenStr = " * ".join(
                [
                    str(primZahl)
                    for primZahlListe in gemeinsamePrimzahlenMatrix
                    for primZahl in primZahlListe
                ]
            )
            if len(gemeinsamePrimzahlenStr.strip()) == 0:
                gemeinsamePrimzahlenStr = "1"
            from functools import reduce

            try:
                grGv = reduce(
                    lambda x, y: x * y,
                    [
                        primZahl
                        for primZahlListe in gemeinsamePrimzahlenMatrix
                        for primZahl in primZahlListe
                    ],
                )
            except TypeError:
                grGv = 1

            if len(bereiche) > 1 or not (
                Txt.hasWithoutABC({i18n.befehle2["p"]})
                or Txt.hasWithoutABC({i18n.befehle2["mulpri"]})
            ):
                print(
                    i18n.gemeinsamkeitenWort
                    + ": {} := {}".format(grGv, gemeinsamePrimzahlenStr)
                )
                for zahl, hierUnwichtig in bereiche.items():
                    dazu = " * ".join(
                        [str(p) for p in primfaktoren(round(zahl / grGv))]
                    )
                    print(
                        f"{round(zahl / grGv):<5} := {zahl:<5} / {grGv:<5} -> "
                        + (dazu if len(dazu.strip()) > 0 else "1")
                    )
            # print("Unterschiede: {}".format(d))

        if Txt.hasWithoutABC({i18n.befehle2["prim"], i18n.befehle2["primfaktorzerlegung"]}):
            for arg in BereichToNumbers2(zahlenReiheKeineWteiler, False, 0):
                cmd_gave_output = True
                print(
                    str(arg)
                    + ": "
                    + str(primRepeat(primfaktoren(int(arg))))[1:-1]
                    .replace("'", "")
                    .replace(", ", " ")
                )

        if Txt.hasWithoutABC({i18n.befehle2["multis3"]}) > 0:
            cmd_gave_output = True

            listeStrWerte = BereichToNumbers2(zahlenReiheKeineWteiler, False, 0)
            mult3arg, mult3m3 = mult3(listeStrWerte)
            print(str(mult3arg) + ": " + str(list(mult3m3)))

        if Txt.hasWithoutABC({i18n.befehle2["multis"]}) > 0:
            cmd_gave_output = True

            listeStrWerte = list(BereichToNumbers2(zahlenReiheKeineWteiler, False, 0))
            multiplesTexts, multiis = mult2(listeStrWerte)
            mulpriInfo = not (Txt.hasWithoutABC({i18n.befehle2["mulpri"]}) or Txt.hasWithoutABC({i18n.befehle2["p"]}))
            for i, (texxt, multii) in enumerate(zip(multiplesTexts, multiis)):
                if len(multii) > 0 or mulpriInfo:
                    print(texxt)
                else:
                    StrZahl = str(listeStrWerte[i])
                    print("".join((StrZahl,": ", StrZahl, " (", i18n.primzahlWort, ")")))

            # externCommand(i18n.befehle2["prim"], c)

        if len({i18n.befehle2["mond"]} & Txt.mengeE) > 0:
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                [
                    "".join(
                        (
                            "--",
                            i18n.ParametersMain.bedeutung[0],
                            "=",
                            i18n.gestirnWort,
                        )
                    )
                ],
                "3-6",
                Txt,
            )

        if len({i18n.befehle2["modulo"]} & Txt.mengeE) > 0:
            cmd_gave_output = True
            moduloA([str(num) for num in BereichToNumbers2(zahlenBereichC)])
        if len({i18n.befehle2["alles"]} & Txt.mengeE) > 0:
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                ["--" + i18n.ParametersMain.alles[0]],
                None,
                Txt,
            )

        if len({i18n.befehle2["primzahlkreuz"]} & Txt.mengeE) > 0:
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                anotherOberesMaximum(zahlenBereichC, 1028, Txt),
                [
                    "".join(
                        (
                            "--",
                            i18n.ParametersMain.bedeutung[0],
                            "=",
                            i18n.primzahlkreuzWort,
                        )
                    )
                ],
                None,
                Txt,
            )
            import reta

        if Txt.hasWithoutABC({i18n.befehle2["richtung"], i18n.befehle2["r"]}):
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                [
                    "".join(
                        (
                            "--",
                            i18n.ParametersMain.primzahlwirkung[0],
                            "=",
                            i18n.GalaxieabsichtWort,
                        )
                    )
                ],
                None,
                Txt,
            )
        if (
            len(Txt.listeE) > 0
            and any(
                [token[:3] == "16_" and token[:5] != "16_15" for token in Txt.listeE]
            )
            and i18n.befehle2["abc"] not in Txt.listeE
            and i18n.befehle2["abcd"] not in Txt.listeE
        ):
            cmd_gave_output = True
            import reta

            befehle16 = []
            for token in Txt.listeE:
                if token[:3] == "16_":
                    befehle16 += [wahl16[token[3:]]]
            grundstruk = ",".join(befehle16)
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                [
                    "".join(
                        (
                            "--",
                            i18n.ParametersMain.multiversum[0],
                            "=",
                            grundstruk,
                        )
                    )
                ],
                None,
                Txt,
            )
        if (
            len(Txt.listeE) > 0
            and any(
                [token[:3] == "15_" or token[:5] == "16_15" for token in Txt.listeE]
            )
            and i18n.befehle2["abc"] not in Txt.listeE
            and i18n.befehle2["abcd"] not in Txt.listeE
        ):
            cmd_gave_output = True
            import reta

            befehle15 = []
            for token in Txt.listeE:
                try:
                    if token[:3] == "15_":
                        befehle15 += [wahl15[token[3:]]]
                    if token == "16_15":
                        befehle15 += [wahl15["15"]]
                    if token[:6] == "16_15_":
                        befehle15 += [wahl15[token[6:]]]
                except KeyError:
                    pass
            grundstruk = ",".join(befehle15)
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln1,
                zeiln2,
                [
                    "".join(
                        (
                            "--",
                            i18n.ParametersMain.grundstrukturen[0],
                            "=",
                            grundstruk,
                        )
                    )
                ],
                None,
                Txt,
            )
    ifAbst = Txt.hasWithoutABC({i18n.befehle2["abstand"]})
    ifAbstPrim = Txt.hasWithoutABC({i18n.befehle2["abstandPrim"]})
    if (
        ifAbst or ifAbstPrim
    ):
        zBereiche: list = []
        for i, s in enumerate(Txt.liste):
            if isZeilenAngabe(s):
                zBereiche += [s]
        allAreNumbers = all((z.isdecimal() for z in zBereiche))
        def maxMenge(mengen):
            mengen = list(mengen)
            if not mengen:
                return set()
            maxMenge: set = mengen[0]
            for menge in mengen[1:]:
                if len(maxMenge) < len(menge):
                    maxMenge = menge
            return maxMenge

        if len(zBereiche) > 1:
            cmd_gave_output = True
            zeige1 = {}
            zeigeAll1 = {}
            zeige2 = {}
            zeigeAll2 = {}
            zahlenBereiche = set()
            for zB in zBereiche:
                zahlenBereiche |= {frozenset(BereichToNumbers2(zB))}
            for i, zB1 in enumerate(zahlenBereiche):
                for k, zB2 in enumerate(zahlenBereiche - maxMenge(zahlenBereiche)):
                    if zB1 != zB2:
                        for zZahl1 in zB2:
                            if ifAbst:
                                dictionary1 = {zZahl2: abs(zZahl1 - zZahl2) for zZahl2 in zB1}
                                if len(dictionary1.items()) > 1 or allAreNumbers:
                                    zeige1.update(dictionary1)
                                    zeigeAll1.update({zZahl1:str(dictionary1)[1:-1]})
                            if ifAbstPrim:
                                dictionary2 = {zZahl2: primRepeat(primfaktoren(int(abs(zZahl1 - zZahl2)))) for zZahl2 in zB1}
                                if len(dictionary2.items()) > 1 or allAreNumbers:
                                    zeige2.update(dictionary2)
                                    zeigeAll2.update({zZahl1:str(dictionary2)[1:-1]})
            for i, (key, value) in enumerate(zeigeAll1.items()):
                print(str(key)+"->: "+value)
            for i, (key, value) in enumerate(zeigeAll2.items()):
                print(str(key)+"->: "+value)

        elif Txt.hasWithoutABC({i18n.befehle2["abstand"]}):
            print(i18nRP.abstandMeldung)

    loggingSwitch, cmd_gave_output = PromptVonGrosserAusgabeSonderBefehlAusgaben(
        loggingSwitch, Txt, cmd_gave_output
    )
    if len(nurEinBefehl) > 0:
        Txt.liste = list(befehleBeenden)
        nurEinBefehl = " ".join(befehleBeenden)
        exit()
    if (
        not cmd_gave_output
        and len(Txt.liste) > 0
        and Txt.listeE[0] not in befehleBeenden
    ):
        if len(Txt.menge & set(befehle)) > 0:
            print(i18nRP.out1Saetze[0] + " ".join(Txt.listeE) + i18nRP.out1Saetze[1])
        else:
            print(i18nRP.out2Satz.format(" ".join(Txt.listeE)))
    return loggingSwitch


def retaCmdAbstraction_n_and_1pron(
    condition,
    paras,
    paras2,
    selectedCols,
    Txt,
    bruch_GanzZahlReziproke,
    zahlenBereichC,
    ketten,
    cmd_gave_output,
    zeiln1,
    zeiln2,
    zeiln3,
    zeiln4,
):
    """abstraction for commands giving results forr n and 1/n"""
    was_n_1proN_cmd = False
    if condition and (
        i18n.befehle2["abc"] not in Txt.listeE
        and i18n.befehle2["abcd"] not in Txt.listeE
    ):
        was_n_1proN_cmd = True
        if len(zahlenBereichC) > 0:
            cmd_gave_output = True
            retaExecuteNprint(
                ketten, Txt.listeE, zeiln1, zeiln2, paras, selectedCols[0], Txt
            )
        if (
            len(bruch_GanzZahlReziproke) > 0
            and textHatZiffer(bruch_GanzZahlReziproke)
            and zeiln3 != ""
        ):
            cmd_gave_output = True
            retaExecuteNprint(
                ketten,
                Txt.listeE,
                zeiln3,
                zeiln4,
                paras if paras2 in [None, [], ()] else paras2,
                selectedCols[1],
                Txt,
            )
    return was_n_1proN_cmd, cmd_gave_output


def ifPrintCmdAgain(Txt):
    return (
        "".join(("--", i18n.ausgabeParas["art"], "=", i18n.ausgabeArt["bbcode"]))
        in Txt.listeE
        # and "reta" == Txt.listeE[0]
    )


def zeiln1234create(
    Txt,
    bedingungZahl,
    bruch_GanzZahlReziproke,
    zahlenBereichC,
    maxNum,
    zahlenReiheKeineWteiler,
):
    if len(bruch_GanzZahlReziproke) > 0 and textHatZiffer(bruch_GanzZahlReziproke):
        zeiln3 = vorherVonAusschnittOderZaehlung(Txt, bruch_GanzZahlReziproke)
        zeiln4 = ""
    else:
        zeiln3 = "".join(("--", i18n.zeilenParas["vorhervonausschnitt"], "=0"))
        zeiln4 = ""
    if bedingungZahl:
        zahlenBereiche = str(zahlenBereichC).strip()
        if textHatZiffer(zahlenBereiche):
            if i18n.befehle2["einzeln"] not in Txt.listeE and (
                (i18n.befehle2["vielfache"] in Txt.listeE)
                or (
                    i18n.befehle2["v"] in Txt.listeE
                    and i18n.befehle2["abc"] not in Txt.listeE
                    and i18n.befehle2["abcd"] not in Txt.listeE
                )
            ):
                if (
                    zahlenReiheKeineWteiler[0] == "("
                    and zahlenReiheKeineWteiler[-1] == ")"
                ):
                    zahlenReiheKeineWteiler[0] == "["
                    zahlenReiheKeineWteiler[-1] == "]"
                if (
                    zahlenReiheKeineWteiler[0] == "["
                    and zahlenReiheKeineWteiler[-1] == "]"
                ) or (
                    zahlenReiheKeineWteiler[0] == "{"
                    and zahlenReiheKeineWteiler[-1] == "}"
                ):
                    zahlenReiheKeineWteiler2 = ",".join(
                        [
                            str(B)
                            for B in BereichToNumbers2(zahlenReiheKeineWteiler)
                            if B != 0
                        ]
                    )

                else:
                    zahlenReiheKeineWteiler2 = zahlenReiheKeineWteiler

                if len(Txt.menge & {i18n.befehle2["teiler"], i18n.befehle2["w"]}) == 0:
                    zeiln1 = (
                        "".join(("--", i18n.zeilenParas["vielfachevonzahlen"], "="))
                        + zahlenReiheKeineWteiler2
                    )
                else:
                    zeiln1 = ""
                zeiln2 = "".join(
                    [
                        vorherVonAusschnittOderZaehlung(Txt, zahlenBereiche),
                        ",",
                        ",".join(
                            [
                                i18n.befehle2["v"] + str(z)
                                for z in re.split(
                                    kpattern,
                                    zahlenReiheKeineWteiler2,
                                )
                            ]
                        ),
                    ]
                )

                # zeiln2 = ""
            else:
                zeiln1 = vorherVonAusschnittOderZaehlung(Txt, zahlenBereiche)
                zeiln2 = anotherOberesMaximum(zahlenBereichC, maxNum, Txt)
        else:
            zeiln1 = "".join(("--", i18n.zeilenParas["vorhervonausschnitt"], "=0"))
            zeiln2 = ""

    else:
        zeiln1 = ""
        zeiln2 = ""

    return zeiln1, zeiln2, zeiln3, zeiln4


def retaExecuteNprint(
    ketten: list,
    stextE,
    zeiln1: str,
    zeiln2: str,
    welcheSpalten: list,
    ErlaubteSpalten: str,
    Txt: TXT,
):
    import reta

    kette = [
        "reta",
        "".join(("-", i18n.hauptForNeben["zeilen"])),
        zeiln1,
        zeiln2,
        ("--"+i18n.zeilenParas["invertieren"] if i18n.befehle2["invertieren"] in stextE else ""),
        "".join(("-", i18n.hauptForNeben["spalten"])),
        "".join(welcheSpalten),
        "".join(("--", i18n.ausgabeParas["breite"], "=0")),
        "".join(("-", i18n.hauptForNeben["ausgabe"])),
        "".join(
            (
                "--",
                i18n.ausgabeParas["spaltenreihenfolgeundnurdiese"],
                "=",
                ErlaubteSpalten,
            )
        )
        if ErlaubteSpalten is not None
        else "",
        *[
            "--" + i18n.ausgabeParas["keineleereninhalte"]
            if i18n.befehle2["keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"]
            in stextE
            else ""
        ],
    ] + returnOnlyParasAsList(stextE)
    kette += ketten
    for el in kette:
        vorhervonaus: set = set()
        if i18n.zeilenParas["vorhervonausschnitt"]+"=" in el:
            vorhervonaus |= {el}
    if len(vorhervonaus) > 1:
        kette.remove(i18n.zeilenParas["vorhervonausschnitt"]+"=0")


    if (
        i18n.befehle2["keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"]
        not in stextE
    ):
        if ifPrintCmdAgain(Txt):
            if "--" + i18n.ausgabeParas["nocolor"] in stextE:
                print("[code]" + (" ".join(kette)) + "[/code]")
            else:
                cliout("[code]" + (" ".join(kette)) + "[/code]", True, i18n.ausgabeArt["bbcode"])
        else:
            if "--" + i18n.ausgabeParas["nocolor"] in stextE:
                print(" ".join(kette))
            else:
                cliout(" ".join(kette), True)
    reta.Program(kette, Txt=Txt)


def findEqualNennerZaehler(hierBereich, nenner, nennerZaehlerGleich):
    hierBereich2 = BereichToNumbers2(str(hierBereich))
    nenner2 = BereichToNumbers2(str(nenner))
    for nn3 in nenner2:
        for hB3 in hierBereich2:
            if nn3 == hB3 and nn3 not in [0, 1]:
                nennerZaehlerGleich += [str(nn3)]
    return nennerZaehlerGleich


def findNennerZaehlerMakesWholeNum(
    zaehler, nenner, wholeNumList, wholeNumListReziproke
):
    zaehler2 = BereichToNumbers2(str(zaehler))
    nenner2 = BereichToNumbers2(str(nenner))
    for nn3 in nenner2:
        for zz3 in zaehler2:
            ratNumRez: Fraction = Fraction(zz3, nn3)
            ratNum: Fraction = Fraction(nn3, zz3)
            if int(ratNum) == ratNum:
                wholeNumList += [str(int(ratNum))]
            if int(ratNumRez) == ratNumRez:
                wholeNumListReziproke += [str(int(ratNumRez))]
    return wholeNumList, wholeNumListReziproke


def bruchBereichsManagementAndWbefehl(zahlenBereichC, stext, zahlenAngaben_):
    bruch_GanzZahlReziproke = []
    bruch_GanzZahlReziprokeAbzug = []
    bruch_KeinGanzZahlReziproke = {}
    bruch_KeinGanzZahlReziprokeAbzug = {}
    bruch_KeinGanzZahlReziprok_ = []
    fullBlockIsZahlenbereichAndBruch = True
    rangesBruecheDict = {}
    rangesBruecheDictReverse: dict = {}
    bruch_KeinGanzZahlReziprokeEnDictAbzug = {}
    bruchRanges3Abzug = {}
    valueLenSum = 0
    zahlenAngaben_mehrere = []
    Minusse = {}
    pfaue = {}
    pfaueAbzug = {}
    # alxp(stext)
    for g, a in enumerate(stext):
        bruchAndGanzZahlEtwaKorrekterBereich = []
        bruchBereichsAngaben = []
        bruchRanges = []
        abzug = False
        if a[:1] != "-":
            for etwaBruch in custom_split2(a, ","):
                bruchRange, bruchBereichsAngabe = createRangesForBruchLists(
                    bruchSpalt(etwaBruch)
                )
                (
                    bruchAndGanzZahlEtwaKorrekterBereich,
                    bruchBereichsAngaben,
                    bruchRanges,
                    zahlenAngaben_,
                    etwaAllTrue,
                ) = verifyBruchNganzZahlBetweenCommas(
                    bruchAndGanzZahlEtwaKorrekterBereich,
                    bruchBereichsAngabe,
                    bruchBereichsAngaben,
                    bruchRange,
                    bruchRanges,
                    etwaBruch,
                    zahlenAngaben_,
                )
                if etwaAllTrue:
                    fullBlockIsZahlenbereichAndBruch = (
                        fullBlockIsZahlenbereichAndBruch
                        and all(bruchAndGanzZahlEtwaKorrekterBereich)
                    )

            if fullBlockIsZahlenbereichAndBruch:
                for bruchBereichsAngabe, bruchRange in zip(
                    bruchBereichsAngaben, bruchRanges
                ):
                    if isZeilenAngabe(bruchBereichsAngabe):
                        bruchRange = {b for b in bruchRange if b > 0}
                        EinsInBereichHier1 = BereichToNumbers2(bruchBereichsAngabe)
                        EinsInBereichHier = 1 in EinsInBereichHier1
                        if (
                            bruchBereichsAngabe[:1] == "-"
                            or bruchBereichsAngabe[:2] == i18n.befehle2["v"] + "-"
                        ):
                            minusHier = True
                            if bruchBereichsAngabe[:2] == i18n.befehle2["v"] + "-":
                                pass
                            if bruchBereichsAngabe[:1] == "-":
                                pass
                        else:
                            minusHier = False
                        if 1 in bruchRange:
                            if minusHier:
                                bruch_GanzZahlReziprokeAbzug += [bruchBereichsAngabe]
                            else:
                                bruch_GanzZahlReziproke += [bruchBereichsAngabe]
                        bruchRangeOhne1 = frozenset(set(bruchRange) - {1})
                        neuerBereich = ",".join(
                            {str(zahl) for zahl in EinsInBereichHier1} - {"1"}
                        )
                        Minusse[tuple(bruchRange)] = minusHier
                        if len(bruchRangeOhne1) > 0:
                            if minusHier:
                                try:
                                    bruch_KeinGanzZahlReziprokeAbzug[
                                        bruchRangeOhne1
                                    ] += [bruchBereichsAngabe]
                                    pfaueAbzug[bruchRangeOhne1] += [
                                        bruchBereichsAngabe[:1] == i18n.befehle2["v"]
                                    ]
                                except KeyError:
                                    bruch_KeinGanzZahlReziprokeAbzug[
                                        bruchRangeOhne1
                                    ] = [bruchBereichsAngabe]
                                    pfaueAbzug[bruchRangeOhne1] = [
                                        bruchBereichsAngabe[:1] == i18n.befehle2["v"]
                                    ]
                            else:
                                try:
                                    bruch_KeinGanzZahlReziproke[bruchRangeOhne1] += [
                                        neuerBereich
                                    ]
                                    pfaue[bruchRangeOhne1] += [
                                        bruchBereichsAngabe[:1] == i18n.befehle2["v"]
                                    ]
                                except KeyError:
                                    bruch_KeinGanzZahlReziproke[bruchRangeOhne1] = [
                                        neuerBereich
                                    ]
                                    pfaue[bruchRangeOhne1] = [
                                        bruchBereichsAngabe[:1] == i18n.befehle2["v"]
                                    ]
                        if EinsInBereichHier:
                            neueRange = ",".join([str(zahl) for zahl in bruchRange])
                            stext += [neueRange]
                            EsGabzahlenAngaben = True
                            zahlenAngaben_mehrere += [neueRange]
        zahlenAngaben_mehrere = list(set(zahlenAngaben_ + zahlenAngaben_mehrere))
        # x("zahlenAngaben_mehrere", zahlenAngaben_mehrere)
    try:
        EsGabzahlenAngaben
    except UnboundLocalError:
        EsGabzahlenAngaben = False
    if (i18n.befehle2["v"] in stext) or (i18n.befehle2["vielfache"] in stext):
        if not (
            (i18n.befehle2["e"] in stext)
            or (
                i18n.befehle2["keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"]
                in stext
            )
        ):
            if (
                len(bruch_GanzZahlReziproke) > 0
                or any(
                    [
                        any([1 in BereichToNumbers2(val2) for val2 in val])
                        for val in bruch_KeinGanzZahlReziproke.values()
                    ]
                )
                or EsGabzahlenAngaben
            ):
                print(i18nRP.out3Saetze)
        bdNeu = set()
        for bDazu in bruch_GanzZahlReziproke:
            for bDazu in BereichToNumbers2(bDazu):
                i = 1
                rechnung = i * bDazu
                while rechnung < retaProgram.tables.hoechsteZeile[1024]:
                    bdNeu |= {rechnung}
                    i += 1
                    rechnung = i * bDazu
        for bDazu in bruch_GanzZahlReziprokeAbzug:
            if bDazu[:1] == i18n.befehle2["v"]:
                bDazu = bDazu[1:]
            if bDazu[:1] == "-":
                bDazu = bDazu[1:]
            for bDazu in BereichToNumbers2(bDazu):
                i = 1
                rechnung = i * bDazu
                while rechnung < retaProgram.tables.hoechsteZeile[1024]:
                    try:
                        bdNeu -= {rechnung}
                        i += 1
                        rechnung = i * bDazu
                    except:
                        pass
        bruch_GanzZahlReziproke = ",".join((str(b) for b in bdNeu))
        bruchRanges3 = {}
        bruch_KeinGanzZahlReziprokeEnDict = {}
        for k, (brZahlen, no1brueche) in enumerate(bruch_KeinGanzZahlReziproke.items()):
            for no1bruch in no1brueche:
                if len(no1bruch) > 0 and no1bruch[0] == i18n.befehle2["v"]:
                    no1bruch = no1bruch[1:]
                if len(no1bruch) > 0 and no1bruch[0] == "-":
                    no1bruch = no1bruch[1:]
                    abzug = True
                else:
                    abzug = False
                no1brueche = BereichToNumbers2(no1bruch)
                for no1bruch in no1brueche:
                    i = 1
                    rechnung2 = no1bruch * i
                    while rechnung2 in gebrochenErlaubteZahlen:
                        if rechnung2 not in bruch_KeinGanzZahlReziprokeEnDict.values():
                            if abzug:
                                try:
                                    bruch_KeinGanzZahlReziprokeEnDictAbzug[k] += [
                                        rechnung2
                                    ]
                                except KeyError:
                                    bruch_KeinGanzZahlReziprokeEnDictAbzug[k] = [
                                        rechnung2
                                    ]
                            else:
                                try:
                                    bruch_KeinGanzZahlReziprokeEnDict[k] += [rechnung2]
                                except KeyError:
                                    bruch_KeinGanzZahlReziprokeEnDict[k] = [rechnung2]
                        i += 1
                        rechnung2 = no1bruch * i
            for br in brZahlen:
                i = 1
                rechnung = br * i
                while rechnung in gebrochenErlaubteZahlen:
                    if abzug:
                        try:
                            if rechnung not in bruchRanges3Abzug:
                                bruchRanges3Abzug[k] += [rechnung]
                        except KeyError:
                            bruchRanges3Abzug[k] = [rechnung]
                    else:
                        try:
                            if rechnung not in bruchRanges3:
                                bruchRanges3[k] += [rechnung]
                        except KeyError:
                            bruchRanges3[k] = [rechnung]
                    i += 1
                    rechnung = br * i

        for keyRanges, valueRanges in bruchRanges3.items():
            for (
                keyBrueche,
                valueBrueche,
            ) in bruch_KeinGanzZahlReziprokeEnDict.items():
                for eineRange in valueRanges:
                    for einBruch in valueBrueche:
                        if keyRanges == keyBrueche:
                            try:
                                strBruch = str(einBruch)
                                if strBruch not in rangesBruecheDict[eineRange]:
                                    rangesBruecheDict[eineRange] += [strBruch]
                            except KeyError:
                                rangesBruecheDict[eineRange] = [str(einBruch)]
        if len(bruchRanges3Abzug) > 0:
            rangesBruecheDict2 = deepcopy(rangesBruecheDict)
            for AbzugNenners, AbzugZaehlers in zip(
                bruchRanges3Abzug.values(),
                bruch_KeinGanzZahlReziprokeEnDictAbzug.values(),
            ):
                for aNenner, aZaehler in zip(AbzugNenners, AbzugZaehlers):
                    for key, value in zip(
                        bruchRanges3.values(), rangesBruecheDict.values()
                    ):
                        try:
                            if key.index(int(aNenner)) == value.index(str(aZaehler)):
                                try:
                                    value.remove(str(aZaehler))
                                except:
                                    pass
                                try:
                                    key.remove(str(aNenner))
                                except:
                                    pass
                                try:
                                    value.remove(aZaehler)
                                except:
                                    pass
                                try:
                                    key.remove(aNenner)
                                except:
                                    pass
                                rangesBruecheDict2[aNenner] = value
                        except ValueError:
                            pass
            rangesBruecheDict = rangesBruecheDict2
            bruchRanges3Abzug = {}
            bruch_KeinGanzZahlReziprokeEnDictAbzug = {}
    else:
        if (
            len(bruch_GanzZahlReziproke) == 0
            or type(bruch_GanzZahlReziproke) is not str
        ):
            bruch_GanzZahlReziproke = ",".join(
                (
                    ",".join(bruch_GanzZahlReziproke),
                    ",".join(bruch_GanzZahlReziprokeAbzug),
                )
            )
        elif type(bruch_GanzZahlReziproke) is str:
            bruch_GanzZahlReziproke += "," + (
                ",".join(
                    (
                        ",".join(bruch_GanzZahlReziproke),
                        ",".join(bruch_GanzZahlReziprokeAbzug),
                    )
                )
            )

        bruchDict = {}
        for (bruchRange, bruch_KeinGanzZahlReziprok_), pfauList in zip(
            bruch_KeinGanzZahlReziproke.items(), pfaue.values()
        ):
            bruch_KeinGanzZahlReziprok_2 = set()
            for pfau, nenners in zip(pfauList, bruch_KeinGanzZahlReziprok_):
                if pfau:
                    nenners = BereichToNumbers2(nenners)
                    for nenner in nenners:
                        i = 1
                        rechnung = i * int(nenner)
                        while rechnung in gebrochenErlaubteZahlen:
                            bruch_KeinGanzZahlReziprok_2 |= {str(rechnung)}
                            i += 1
                            rechnung = i * int(nenner)
                else:
                    bruch_KeinGanzZahlReziprok_2 |= set(re.split(kpattern, nenners))
            bruch_KeinGanzZahlReziprok_ = ",".join(bruch_KeinGanzZahlReziprok_2)
            for rangePunkt in bruchRange:
                try:
                    bruchDict[rangePunkt] |= {bruch_KeinGanzZahlReziprok_}
                except KeyError:
                    bruchDict[rangePunkt] = {bruch_KeinGanzZahlReziprok_}

                for (
                    bruchRangeA,
                    bruch_KeinGanzZahlReziprok_A,
                ) in bruch_KeinGanzZahlReziprokeAbzug.items():
                    bruch_KeinGanzZahlReziprok_A = ",".join(
                        bruch_KeinGanzZahlReziprok_A
                    )
                    for rangePunktA in bruchRangeA:
                        if rangePunkt == rangePunktA:
                            try:
                                bruchDict[rangePunkt] |= {
                                    bruch_KeinGanzZahlReziprok_,
                                    bruch_KeinGanzZahlReziprok_A,
                                }
                            except KeyError:
                                bruchDict[rangePunkt] = {
                                    bruch_KeinGanzZahlReziprok_,
                                    bruch_KeinGanzZahlReziprok_A,
                                }
        rangesBruecheDict = bruchDict
    rangesBruecheDict2 = {}
    bereicheVorherBestimmtSet = set()
    for key, values in rangesBruecheDict.items():
        bereichVorherBestimmt = [BereichToNumbers2(value) for value in values]
        bereicheVorherBestimmtSet2 = set()
        for b in bereichVorherBestimmt:
            bereicheVorherBestimmtSet2 |= b
        bereicheVorherBestimmtSet |= bereicheVorherBestimmtSet2
        rangesBruecheDict2[key] = list(bereicheVorherBestimmtSet2)
    valueLenSum += len(bereicheVorherBestimmtSet)
    dictLen = len(rangesBruecheDict)
    if dictLen != 0:
        avg = valueLenSum / dictLen
        if avg < 1:
            rangesBruecheDictReverse = invert_dict_B(rangesBruecheDict2)
            rangesBruecheDict = {}
    zahlenAngaben_mehrere = list(set(zahlenAngaben_mehrere))
    if len(zahlenAngaben_mehrere) > 0:
        zahlenAngaben_mehrereStr = ",".join(zahlenAngaben_mehrere)
        zahlenReiheKeineWteiler = copy(zahlenAngaben_mehrereStr)
        if i18n.befehle2["w"] in stext or i18n.befehle2["teiler"] in stext:
            zahlenAngaben_mehrereStr = ",".join(
                [
                    str(zahl)
                    for zahl in BereichToNumbers2(
                        ",".join(
                            [
                                str(z).split("+")[0]
                                for z in re.split(
                                    kpattern,
                                    zahlenReiheKeineWteiler,
                                )
                            ]
                        ),
                        False,
                        0,
                    )
                ]
            )
            zahlenBereichC: str = ",".join(teiler(zahlenAngaben_mehrereStr)[0])
            if len(zahlenReiheKeineWteiler) > 1:
                zahlenBereichC += "," + zahlenReiheKeineWteiler
        else:
            zahlenBereichC = zahlenAngaben_mehrereStr

    try:
        zahlenReiheKeineWteiler
    except (UnboundLocalError, NameError):
        zahlenReiheKeineWteiler = ""

    dazu = []
    sdazu = []
    bruch_GanzZahlReziprokeDazu = []
    EsGabzahlenAngaben, bruch_GanzZahlReziprokeDazu, dazu, sdazu = addMoreVals2(
        EsGabzahlenAngaben,
        bruch_GanzZahlReziprokeDazu,
        dazu,
        rangesBruecheDict,
        sdazu,
        False,
    )
    EsGabzahlenAngaben, bruch_GanzZahlReziprokeDazu, dazu, sdazu = addMoreVals2(
        EsGabzahlenAngaben,
        bruch_GanzZahlReziprokeDazu,
        dazu,
        rangesBruecheDictReverse,
        sdazu,
        True,
    )

    if len(dazu) > 0:
        zahlenBereichC = ",".join(
            filter(None, sdazu + re.split(kpattern, zahlenBereichC))
        )
        stext += [",".join(sdazu + dazu)]
        bruch_GanzZahlReziproke = ",".join(
            filter(
                None,
                bruch_GanzZahlReziprokeDazu
                + re.split(kpattern, bruch_GanzZahlReziproke),
            )
        )

    return (
        bruch_GanzZahlReziproke,
        zahlenBereichC,
        zahlenReiheKeineWteiler,
        fullBlockIsZahlenbereichAndBruch,
        rangesBruecheDict,
        len(zahlenAngaben_) > 0 or EsGabzahlenAngaben,
        rangesBruecheDictReverse,
        stext,
    )


def addMoreVals2(
    EsGabzahlenAngaben,
    bruch_GanzZahlReziprokeDazu,
    dazu,
    rangesBruecheOrReverseDict,
    sdazu,
    ifReverse,
):
    for key, values in rangesBruecheOrReverseDict.items():
        key = int(key)
        if key != 0:
            for value in BereichToNumbers2(",".join(values)):
                if value != 0:
                    bruch2 = (
                        Fraction(key, value) if not ifReverse else Fraction(value, key)
                    )
                    (
                        EsGabzahlenAngaben,
                        bruch_GanzZahlReziprokeDazu,
                        dazu,
                        sdazu,
                    ) = addMoreVals(
                        EsGabzahlenAngaben,
                        bruch2,
                        bruch_GanzZahlReziprokeDazu,
                        dazu,
                        sdazu,
                    )
    return EsGabzahlenAngaben, bruch_GanzZahlReziprokeDazu, dazu, sdazu


def addMoreVals(EsGabzahlenAngaben, bruch2, bruch_GanzZahlReziprokeDazu, dazu, sdazu):
    if bruch2.numerator % bruch2.denominator == 0:
        dazu += [str(int(bruch2))]
        sdazu += [str(int(bruch2))]
        EsGabzahlenAngaben = True
    if bruch2.denominator % bruch2.numerator == 0:
        dazu += ["1/" + str(int(bruch2**-1))]
        bruch_GanzZahlReziprokeDazu += [str(int(bruch2**-1))]
    return EsGabzahlenAngaben, bruch_GanzZahlReziprokeDazu, dazu, sdazu


def PromptVonGrosserAusgabeSonderBefehlAusgaben(loggingSwitch, Txt, cmd_gave_output):
    if (
        len(Txt.listeS) > 0
        and Txt.listeS[0] == i18n.befehle2["shell"]
        and not (
            Txt.has({i18n.befehle2["abc"], i18n.befehle2["abcd"]})
            and len(Txt.liste) == 2
        )
    ):
        cmd_gave_output = True
        try:
            process = subprocess.Popen([*Txt.listeS[1:]])
            process.wait()
        except:
            pass
    if (
        len(Txt.listeS) > 0
        and i18n.befehle2["python"] == Txt.listeS[0]
        and not (
            Txt.has({i18n.befehle2["abc"], i18n.befehle2["abcd"]})
            and len(Txt.liste) == 2
        )
    ):
        cmd_gave_output = True
        try:
            process = subprocess.Popen(["python3", "-c", " ".join(Txt.listeS[1:])])
            process.wait()
        except:
            pass
    if len(Txt.listeS) > 0 and i18n.befehle2["math"] == Txt.listeS[0]:
        cmd_gave_output = True
        for st in re.split(kpattern, "".join(Txt.listeS[1:2])):
            try:
                process = subprocess.Popen(["python3", "-c", "print(" + st + ")"])
                process.wait()
            except:
                pass
    if Txt.hasWithoutABC({i18n.befehle2["loggen"]}):
        cmd_gave_output = True
        loggingSwitch = True
    elif Txt.hasWithoutABC({i18n.befehle2["nichtloggen"]}):
        cmd_gave_output = True
        loggingSwitch = False
    return loggingSwitch, cmd_gave_output


def verdreheWoReTaBefehl(text1: str, text2: str, text3: str, PromptMode: PromptModus):
    if text2[:4] == "reta" and text1[:4] != "reta" and len(text3) > 0:
        return text2, text1, custom_split(text2)
    return text1, text2, text3

spaltenParaNvalueS: dict = {"zeilen": {},"spalten": {}, "ausgabe": {}, "kombination": {}}

def regExReplace(Txt) -> list:
    if not any(("r\"" in a or "*" in a for a in Txt.menge)):
        return Txt.liste
    ifReta: bool = True if Txt.liste[:1] == ["reta"] else False
    neueListe: list = []
    foundParas4value: list = []
    i: int = -1
    regexAufgeloest = False
    changedAtAll = False
    def lastRetaHauptPara() -> str:
        for el in reversed(neueListe):
            if el[:1] == "-" and el[:2] != "--":
                try:
                    return el[1:]
                except:
                    return ""
        return ""
    def allEqSignAbarbeitung(foundParas4value, hauptCmd,onlyGen = False, eqThing=""):
        spaltenParaNvalue: dict = {}
        newTokens: list = []
        if hauptCmd == i18n.hauptForNeben["spalten"]:
            if len(spaltenParaNvalueS["spalten"]) == 0:
                for liste1 in retaProgram.dataDict[0].values():
                    for liste2 in liste1:
                        for liste3 in liste2:
                            try:
                                spaltenParaNvalue[liste3[0]] |= {liste3[1]}
                            except KeyError:
                                spaltenParaNvalue[liste3[0]] = {liste3[1]}
                spaltenParaNvalueS["spalten"] = spaltenParaNvalue
            else:
                spaltenParaNvalue = spaltenParaNvalueS["spalten"]
        elif hauptCmd == i18n.hauptForNeben["zeilen"]:
            if len(spaltenParaNvalueS["zeilen"]) == 0:
                spaltenParaNvalue = {zeilenPara: {''} for zeilenPara in i18n.haupt2neben[i18n.hauptForNeben["zeilen"]]}
                spaltenParaNvalue[i18n.zeilenParas["zeit"]] = {i18n.zeilenParas["gestern"], i18n.zeilenParas["heute"], i18n.zeilenParas["morgen"]}
                spaltenParaNvalue[i18n.zeilenParas["typ"]] = {i18n.zeilenParas["mond"],
                                                          i18n.zeilenParas["sonne"],
                                                          i18n.zeilenParas["planet"],
                                                          i18n.zeilenParas["schwarzesonne"],
                                                          i18n.zeilenParas["SonneMitMondanteil"]}
                spaltenParaNvalue[i18n.zeilenParas["primzahlen"]] = {i18n.zeilenParas["aussenerste"], i18n.zeilenParas["innenerste"], i18n.zeilenParas["innenalle"], i18n.zeilenParas["aussenalle"]}
                spaltenParaNvalueS["zeilen"] = spaltenParaNvalue
            else:
                spaltenParaNvalue = spaltenParaNvalueS["zeilen"]
        elif hauptCmd == i18n.hauptForNeben["kombination"]:
            if len(spaltenParaNvalueS["kombination"]) == 0:
                spaltenParaNvalue = {i18n.kombiMainParas["galaxie"]: {text for tupel in i18n.kombiParaNdataMatrix.values() for text in tupel}, i18n.kombiMainParas["universum"]: {text for tupel in i18n.kombiParaNdataMatrix2.values() for text in tupel}}
                spaltenParaNvalueS["kombination"] = spaltenParaNvalue
            else:
                spaltenParaNvalue = spaltenParaNvalueS["kombination"]
        elif hauptCmd == i18n.hauptForNeben["ausgabe"]:
            if len(spaltenParaNvalueS["ausgabe"]) == 0:
                spaltenParaNvalue = {ausgabePara: {''} for ausgabePara in i18n.haupt2neben[i18n.hauptForNeben["ausgabe"]]}
                spaltenParaNvalue[i18n.ausgabeParas["art"]] = set(i18n.ausgabeArt.keys())
                eqAusgabeParas = i18n.nested.artWort
                spaltenParaNvalueS["ausgabe"] = spaltenParaNvalue
            else:
                spaltenParaNvalue = spaltenParaNvalueS["ausgabe"]
        if onlyGen:
            return
        if i == 0:
            for para4value in spaltenParaNvalue.keys():
                if any(re.findall(regex, para4value)) or any(re.findall(regex, para4value+"=")):
                    try:
                        foundParas4value += [para4value]
                    except NameError:
                        foundParas4value: list = [para4value]
        elif i == 1:
            if len(eqThing) > 0 and not all([spaltenParaNvalue[a]=={''} for a in foundParas4value]):
                found2: dict = {}
                for found in foundParas4value:
                    passend = [a for a in list(set(spaltenParaNvalue[found]) | set(eqThing)) if len(a) > 1]
                    if len(passend) > 0:
                        found2[found] = passend
                for key, values in found2.items():
                    try:
                        if eqThing in spaltenParaNvalue[key]:
                            newTokens += ["".join(("--",key, "=", eqThing))]
                    except KeyError:
                        pass
            else:
                for para4value in foundParas4value:
                    try:
                        if spaltenParaNvalue[para4value] == {''}:
                            if len(eqThing) > 0:
                                    newTokens += ["".join(("--",para4value, "=", eqThing))]
                            elif all([spaltenParaNvalue[a]=={''} for a in foundParas4value]):
                                newTokens += ["--"+para4value]
                        else:
                            for values4para in spaltenParaNvalue[para4value]:
                                if any(re.findall(regex, values4para)) or any(re.findall(regex, "="+values4para)):
                                    newTokens += ["".join(("--",para4value, "=", values4para))]
                    except KeyError:
                        pass
                foundParas4value = []
        elif i == -1:
            for para4value in [para4value for para4value, value in spaltenParaNvalue.items() if value == {''}]:
                if any(re.findall(regex, para4value)) or any(re.findall(regex, "--"+para4value)):
                    newTokens += ["--"+para4value]
            for haupt in i18n.hauptForNeben.values():
                if any(re.findall(r""+regex, haupt)) or any(re.findall(r""+regex, "-"+haupt)):
                    newTokens += ["-"+haupt]

        regexAufgeloest = True
        return newTokens
    def findregEx(regex, foundParas4value: list = [], eqThing="") -> list:
        def immerHauptParaAbarbeitung(newTokens):
            for haupt in i18n.hauptForNeben.values():
                if (any(re.findall(r""+regex, haupt)) or any(re.findall(r""+regex, "-"+haupt))) and "-"+haupt not in newTokens:
                    newTokens += ["-"+haupt]
            regexAufgeloest = True

        allResultTokens: list = []
        newTokens: list = []
        if ifReta:
            if len(neueListe) > 0:
                if hauptCmd in (i18n.hauptForNeben["kombination"],i18n.hauptForNeben["zeilen"], i18n.hauptForNeben["spalten"], i18n.hauptForNeben["ausgabe"]):
                    newTokens = allEqSignAbarbeitung(foundParas4value, hauptCmd, False, eqThing)
                if len(foundParas4value) == 0 and len(newTokens) == 0:
                    immerHauptParaAbarbeitung(newTokens)
            else:
                return []
        else:
            for el in (cmd for cmd in i18n.befehle2.values() if len(cmd) > 1):
                if any(re.findall(regex, el)):
                    newTokens += [el]
        return newTokens

    for listenToken in Txt.liste:
        eqThings2 = listenToken.split("=")
        hauptCmd = lastRetaHauptPara()
        if len(eqThings2) > 2:
            eqThings2 = [eqThings2[0]] + ["=".join(eqThings2[1:])]
        if len(eqThings2) == 2:
            eqThings: list = [""]
            flag = False
            for i, eqThing7 in enumerate(eqThings2):
                eqThings3 = []
                for eqThing in eqThing7.split(",") if i == 1 else [eqThing7]:
                    if eqThing == "*" or (eqThing in ("--*","--") and i == 0):
                        eqThing = "r\"(.*)\""
                    if eqThing[:2] == "r\"" and eqThing[-1] == "\"":
                        regex = r""+eqThing[2:-1]
                        eqThings3 += findregEx(regex, foundParas4value)
                        flag = True
                        changedAtAll = True
                    else:
                        if flag:
                            eqThings += findregEx(None, foundParas4value, eqThing)
                        else:
                            if "=" not in eqThings[-1]:
                                eqThings[-1] += eqThing + "="
                            else:
                                eqThings[-1] += eqThing
                            foundParas4value += [eqThing[2:]]
                if len(eqThings3) > 0:
                    eqThings += eqThings3
            foundParas4value = []
            neueListe += [" ".join(eqThings)]
        elif listenToken[:2] == "r\"" and listenToken[-1] == "\"":
            regex = r""+listenToken[2:-1]
            i = -1
            neueListe += findregEx(regex)
        else:
            neueListe += [listenToken]
    if changedAtAll:
        neueNeueListe: list = []
        eqThings1: list = []
        eqThings2 = []
        def aufloesen(neueNeueListe, eqThings1, eqThings2, eqWo, ifEnde) -> tuple:
            if len(eqThings1) > 1:
                neueNeueListe += [eqThings1[:-1][0]]
                bis = eqThings2
                neueNeueListe[-1] += ",".join((a for a in bis if len(a) != 0))
            elif len(eqThings1) == 1:
                neueNeueListe += [eqThings1[0]+eqThings2[0]]
            if eqWo == 0:
                eqThings1, eqThings2 = [], []
            else:
                if ifEnde:
                    neueNeueListe += [a+b for a, b in zip(eqThings1, eqThings2)]
                    eqThings1 = []
                    eqThings2 = []

            return neueNeueListe, eqThings1, eqThings2

        neueListe=(" ".join(neueListe)).split()
        for i, n in enumerate(neueListe):
            ifEnde = i+1 == len(neueListe)
            eqWo = n.find("=")+1 # sucht nur nach ErstVorkommen!
            if eqWo != 0:
                if len(eqThings1) == 0:
                    if ifEnde:
                        neueNeueListe += [n]
                    else:
                        eqThings1 += [n[:eqWo]]
                        eqThings2 += [n[eqWo:]]
                elif all((n[:eqWo] == a for a in eqThings1)):
                    eqThings1 += [n[:eqWo]]
                    eqThings2 += [n[eqWo:]]
                    if ifEnde:
                        neueNeueListe += [eqThings1[:-1][0]]
                        neueNeueListe[-1] += ",".join((a for a in eqThings2 if len(a) != 0))
                else:
                    neueNeueListe, eqThings1, eqThings2 = aufloesen(neueNeueListe, eqThings1, eqThings2, eqWo, ifEnde)
                    eqThings1 = [n[:eqWo]]
                    eqThings2 = [n[eqWo:]]
            else:
                neueNeueListe, eqThings1, eqThings2 = aufloesen(neueNeueListe, eqThings1, eqThings2, eqWo, ifEnde)
                neueNeueListe += [n]
        neueListe = neueNeueListe
    if not ifReta and regexAufgeloest:
        print(" ".join(neueListe))
    #exit()
    return neueListe

def promptVorbereitungGrosseAusgabe(
    platzhalter, promptMode, promptMode2, promptModeLast, text, textDazu0
):
    Txt = TXT(text)
    Txt.platzhalter = platzhalter
    ketten = []
    # AusgabeSelektiv = 5
    ifKurzKurz = False
    if len(Txt.liste) > 0:
        textDazu: list = []
        s_2: list
        ifKurzKurz, Txt.liste = stextFromKleinKleinKleinBefehl(
            promptMode2, Txt.liste, textDazu
        )
    if Txt.liste is not None:
        nstextnum: list = []
        for astext in Txt.liste:
            if astext.isdecimal():
                nstextnum += [int(astext)]
        if len(nstextnum) > 0:
            maxNum = max(nstextnum)
        else:
            maxNum = 1024
    zahlenBereichNeu: map = {}
    zahlenBereichNeu1: map = {}
    for swort in Txt.liste:
        try:
            zahlenBereichNeu1[bool(isZeilenAngabe(swort))] += [swort]
        except KeyError:
            zahlenBereichNeu1[bool(isZeilenAngabe(swort))] = [swort]
    for key, value in zahlenBereichNeu1.items():
        zahlenBereichNeu[key] = ",".join(value)

    zahlenBereichMatch = tuple(zahlenBereichNeu.keys())
    if (
        promptMode2 == PromptModus.AusgabeSelektiv
        and promptModeLast == PromptModus.normal
    ):
        Txt.liste = textDazu0 + Txt.liste
    if (
        promptMode == PromptModus.normal
        and len(Txt.platzhalter) > 1
        and Txt.platzhalter[:4] == "reta"
        and any(zahlenBereichMatch)
        and zahlenBereichMatch.count(True) == 1
    ):
        zeilenn = False
        woerterToDel = []
        for i, wort in enumerate(Txt.liste):
            if len(wort) > 1 and wort[0] == "-" and wort[1] != "-":
                zeilenn = False
            if zeilenn is True or wort == zahlenBereichNeu[True]:
                woerterToDel += [i]
            if wort == "-" + i18n.hauptForNeben["zeilen"]:
                zeilenn = True
                woerterToDel += [i]
        stextDict = {i: swort for i, swort in enumerate(Txt.liste)}
        for todel in woerterToDel:
            del stextDict[todel]
        Txt.liste = list(stextDict.values())

        if len({i18n.befehle2["w"], i18n.befehle2["teiler"]} & Txt.menge) > 0:
            BereichMenge = BereichToNumbers2(zahlenBereichNeu[True], False, 0)
            BereichMengeNeu = teiler(",".join([str(b) for b in BereichMenge]))[1]
            zahlenBereichNeu[True] = ""
            for a in BereichMengeNeu:
                zahlenBereichNeu[True] += str(a) + ","
            zahlenBereichNeu[True] = zahlenBereichNeu[True][:-1]

            try:
                tx = Txt.liste
                tx.remove(i18n.befehle2["w"])
                Txt.liste = x
            except:
                pass
            try:
                tx = Txt.liste
                tx.remove(i18n.befehle2["teiler"])
                Txt.liste = x
            except:
                pass

        if len({i18n.befehle2["v"], i18n.befehle2["vielfache"]} & Txt.menge) == 0:
            Txt.liste += [
                "".join(("-", i18n.hauptForNeben["zeilen"])),
                vorherVonAusschnittOderZaehlung(Txt, zahlenBereichNeu[True]),
            ]

        else:
            Txt.liste += [
                "".join(("-", i18n.hauptForNeben["zeilen"])),
                "".join(("--", i18n.zeilenParas["vielfachevonzahlen"], "="))
                + zahlenBereichNeu[True],
            ]
            try:
                tx = Txt.liste
                tx.remove(i18n.befehle2["v"])
                Txt.liste = x
            except:
                pass
            try:
                tx = Txt.liste
                tx.remove(i18n.befehle2["vielfache"])
                Txt.liste = x
            except:
                pass
    IsPureOnlyReTaCmd: bool = len(Txt.liste) > 0 and Txt.liste[0] == "reta"
    brueche = []
    zahlenAngaben_ = []
    zahlenAngabenC = ""
    if Txt.hasWithoutABC(set(befehleBeenden)):
        Txt.liste = [tuple(befehleBeenden)[0]]
        exit()
    replacements = i18nRP.replacements
    if len(Txt.liste) > 0 and Txt.liste[0] not in [
        "reta",
        i18n.befehle2["shell"],
        i18n.befehle2["python"],
        i18n.befehle2["abstand"],
    ]:
        listeNeu: list = []
        for token in Txt.liste:
            try:
                listeNeu += [replacements[token]]
            except KeyError:
                listeNeu += [token]
        Txt.liste = listeNeu
    if Txt.liste[:1] != ["reta"]:
        Txt.liste = list(Txt.menge)
    Txt.liste = regExReplace(Txt)
    return (
        IsPureOnlyReTaCmd,
        brueche,
        zahlenAngabenC,
        ketten,
        maxNum,
        Txt.liste,
        zahlenAngaben_,
        ifKurzKurz,
    )


def PromptAllesVorGroesserSchleife():
    global promptMode2, textDazu0, befehleBeenden
    #if "-" + i18nRP.retaPromptParameter["vi"] not in sys.argv:
    #    retaPromptHilfe()
    if "-" + i18nRP.retaPromptParameter["log"] in sys.argv:
        loggingSwitch = True
    else:
        loggingSwitch = False
    if ("-" + i18nRP.retaPromptParameter["h"] in sys.argv) or (
        "-" + i18nRP.retaPromptParameter["help"] in sys.argv
    ):
        print(i18nRP.helptext)
        exit()
    if "-" + i18nRP.retaPromptParameter["debug"] in sys.argv:
        retaProgram.propInfoLog = True
        if "-" + i18nRP.retaPromptParameter["e"] not in sys.argv:
            x("T", i18nRP.infoDebugAktiv)

    if "-" + i18nRP.retaPromptParameter["befehl"] in sys.argv:
        von = sys.argv.index("-" + i18nRP.retaPromptParameter["befehl"]) + 1
        nurEinBefehl = sys.argv[von:]
    else:
        nurEinBefehl = []
    if "-" + i18nRP.retaPromptParameter["e"] in sys.argv:
        immerEbefehlJa = True
    else:
        immerEbefehlJa = False
    startpunkt1 = NestedCompleter(
        {a: None for a in befehle},
        {},
        ComplSitua.retaAnfang,
        "",
        {
            **{"reta": ComplSitua.retaAnfang},
            **{a: ComplSitua.befehleNichtReta for a in befehle2},
        },
    )
    promptMode = PromptModus.normal
    promptMode2 = PromptModus.normal
    promptDavorDict = defaultdict(lambda: ">")
    promptDavorDict[PromptModus.speichern] = i18nRP.wspeichernWort
    promptDavorDict[PromptModus.loeschenSelect] = i18nRP.wloeschenWort
    textDazu0 = []
    return (
        befehleBeenden,
        loggingSwitch,
        promptDavorDict,
        promptMode,
        startpunkt1,
        nurEinBefehl,
        immerEbefehlJa,
    )


def PromptLoescheVorSpeicherungBefehle(platzhalter, promptMode, text):
    global promptMode2, textDazu0
    TxtZuloeschen = TXT(text)
    TxtLoeschbereiche = TXT(platzhalter)
    loeschbares1 = {i + 1: a for i, a in enumerate(TxtLoeschbereiche.liste)}
    loeschbares2 = {a: i + 1 for i, a in enumerate(TxtLoeschbereiche.liste)}
    flag = False
    if isZeilenAngabe(TxtZuloeschen.text):
        if (
            TxtZuloeschen.text not in loeschbares2.keys()
            or not TxtZuloeschen.text.isdecimal()
        ):
            zuloeschen2 = BereichToNumbers2(TxtZuloeschen.text, False, 0)
            for todel in zuloeschen2:
                try:
                    del loeschbares1[todel]
                except:
                    pass
            TxtLoeschbereiche.platzhalter = " ".join(loeschbares1.values())
        else:
            flag = True
    else:
        flag = True
    if flag:
        zuloeschen2 = set()
        for wort in TxtZuloeschen.liste:
            try:
                TxtLoeschbereiche.liste = list(
                    filter(lambda a: a != wort, TxtLoeschbereiche.liste)
                )
            except:
                pass
        TxtZuloeschen = TXT(",".join(zuloeschen2))
        TxtLoeschbereiche.platzhalter = " ".join(TxtLoeschbereiche.liste)

    promptMode = PromptModus.normal
    return TxtLoeschbereiche.platzhalter, promptMode, TxtZuloeschen.text


def promptSpeicherungB(nochAusageben, promptMode, Txt):
    if promptMode == PromptModus.speicherungAusgaben:
        Txt.text = Txt.platzhalter
    elif promptMode == PromptModus.speicherungAusgabenMitZusatz:
        Txt.text = Txt.platzhalter + " " + nochAusageben
    return Txt


def promptSpeicherungA(ketten, promptMode, Txt):
    if promptMode == PromptModus.speichern:
        ketten, Txt = speichern(ketten, Txt.platzhalter, Txt.text)
    return ketten, Txt


def promptInput(
    loggingSwitch,
    promptDavorDict,
    promptMode,
    startpunkt1,
    Txt,
    nurEinBefehl,
    immerEbefehlJa,
):
    Txt.text="kurzbefehle"
    if len(nurEinBefehl) == 0:
        #session = newSession(loggingSwitch)
        try:
            Txt.befehlDavor = Txt.text
            if True:
                Txt.text =  sys.stdin.readline()
                #if not Txt.text:
                #    time.sleep(0.1)
                #    continue



                #session.prompt(
                # print_formatted_text("Enter HTML: ", sep="", end=""), completer=html_completer
                # ">",
                #[("class:bla", promptDavorDict[promptMode])],
                # completer=NestedCompleter.from_nested_dict(
                #    startpunkt, notParameterValues=notParameterValues
                # ),
                #completer=startpunkt1
                #if not promptMode == PromptModus.loeschenSelect
                #else None,
                #wrap_lines=True,
                #complete_while_typing=True,
                #vi_mode=True
                #if "-" + i18nRP.retaPromptParameter["vi"] in sys.argv
                #else False,
                #style=Style.from_dict({"bla": "#0000ff bg:#ffff00"})
                #if loggingSwitch
                #else Style.from_dict({"bla": "#0000ff bg:#ff0000"}),
                # placeholder="reta",
                #placeholder=Txt.platzhalter,
            #)
            if immerEbefehlJa and Txt.text[:4] != "reta":
                Txt.e = [
                    i18n.befehle2[
                        "keineEinZeichenZeilenPlusKeineAusgabeWelcherBefehlEsWar"
                    ]
                ]
            else:
                Txt.e = []

        except KeyboardInterrupt:
            sys.exit()

    else:
        Txt.text = " ".join(nurEinBefehl)
        Txt.e = []
        Txt.befehlDavor = ""

    return Txt


if __name__ == "__main__":
    PromptScope()


def start(sprachenWahl1="deutsch"):
    global sprachenWahl
    PromptScope()
    return sprachenWahl
