#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import random
import time


class Marktteilnehmer:
    def __init__(self, name):
        self.name = name
        self.geld = random.randint(50, 100)


class Produzent(Marktteilnehmer):
    def produzieren(self):
        kosten = random.randint(1, 10)
        if self.geld >= kosten:
            self.geld -= kosten
            return 1  # Produziert 1 Einheit des Produkts
        return 0


class Konsument(Marktteilnehmer):
    def __init__(self, name):
        super().__init__(name)
        self.nachfrage = random.randint(1, 10)


class Händler(Marktteilnehmer):
    def __init__(self, name):
        super().__init__(name)
        self.angebot = 0


class Markt:
    def __init__(self, produzenten, konsumenten, händler):
        self.produzenten = produzenten
        self.konsumenten = konsumenten
        self.händler = händler
        self.preis = 10
        self.wechselkurs = 1

    def update_angebot_nachfrage(self):
        for produzent in self.produzenten:
            for händler in self.händler:
                händler.angebot += produzent.produzieren()
        gesamt_nachfrage = sum(t.nachfrage for t in self.konsumenten)
        if (
            gesamt_nachfrage > self.händler[0].angebot
        ):  # Hier nehmen wir an, dass es nur einen Händler gibt
            self.preis *= 1.1
        elif gesamt_nachfrage < self.händler[0].angebot:
            self.preis *= 0.9
        self.händler[
            0
        ].angebot = gesamt_nachfrage  # Angebot wird auf die Gesamtnachfrage gesetzt

    def handel(self):
        for i in range(10):  # Simuliert 10 Zeitperioden
            for konsument in self.konsumenten:
                while (
                    konsument.geld >= self.preis
                    and konsument.nachfrage > 0
                    and self.händler[0].angebot > 0
                ):
                    print(
                        f"{konsument.name} kauft ein Produkt für {self.preis} Einheiten."
                    )
                    konsument.geld -= self.preis
                    konsument.nachfrage -= 1
                    self.händler[0].angebot -= 1
            self.update_angebot_nachfrage()
            print(f"Nach Periode {i+1}, der Preis ist jetzt {self.preis}.")
            self.wechselkurs *= random.uniform(0.9, 1.1)  # Wechselkurs fluktuiert
            print(f"Der Wechselkurs ist jetzt {self.wechselkurs}.")
            time.sleep(1)  # Wartet eine Sekunde zwischen jeder Periode

if __name__ == "__main__":
    produzenten = [Produzent(f"Produzent {i}") for i in range(1, 6)]
    konsumenten = [Konsument(f"Konsument {i}") for i in range(1, 6)]
    händler = [Händler(f"Händler {i}") for i in range(1, 2)]  # In diesem Beispiel gibt es nur einen Händler
    markt = Markt(produzenten, konsumenten, händler)
    markt.handel()

"""Hier ist eine Liste von Ideen, mit denen du die Marktsimulation erweitern könntest:

Unterschiedliche Produkte und Dienstleistungen: Füge verschiedene Arten von Produkten und Dienstleistungen hinzu, die die Marktteilnehmer kaufen und verkaufen können.

Angebot und Nachfrage: Implementiere Funktionen, um Angebot und Nachfrage für verschiedene Produkte zu verfolgen und auf der Grundlage dieser Informationen die Preise zu aktualisieren.

Produktionskosten: Füge Kosten für die Produktion von Waren hinzu und berücksichtige diese in der Preisbildung.

Einkommensverteilung: Berücksichtige unterschiedliche Einkommensniveaus der Marktteilnehmer und wie diese das Kaufverhalten beeinflussen.

Spezialisierung: Gib den Marktteilnehmern verschiedene Rollen, wie Produzenten, Konsumenten und Händler, um das Handelssystem zu erweitern.

Verhandlungen: Ermögliche den Marktteilnehmern, Verhandlungen über Preise und andere Handelsbedingungen zu führen.

Transaktionskosten: Füge Transaktionskosten hinzu, die bei jedem Handel anfallen, um realistischere Marktbedingungen abzubilden.

Regierung und Steuern: Implementiere eine Regierung, die Steuern erhebt und öffentliche Güter bereitstellt.

Kredit und Zinsen: Füge ein Banksystem hinzu, das Kredite vergibt und Zinsen erhebt, um Investitionen und Wachstum zu fördern.

Wechselkurse: Wenn mehrere Währungen existieren, implementiere Wechselkurse und erlaube den Marktteilnehmern, Währungen zu tauschen.

Arbeitsmarkt: Erstelle einen Arbeitsmarkt, auf dem Marktteilnehmer Arbeitsplätze suchen und anbieten können, um Einkommen zu erzielen.

Inflation und Deflation: Berücksichtige die Auswirkungen von Inflation und Deflation auf die Kaufkraft der Marktteilnehmer.

Wirtschaftswachstum und Rezession: Implementiere Mechanismen, die Wirtschaftswachstum und Rezessionen simulieren, und beobachte, wie sie das Marktverhalten beeinflussen.

Zeitliche Dimension: Füge eine zeitliche Dimension hinzu, um langfristige Veränderungen und Trends auf dem Markt zu beobachten.

Diese Liste ist nicht erschöpfend, aber sie bietet einige Ideen, um die Simulation komplexer und realistischer zu gestalten. Je nachdem, welche Aspekte der Wirtschaft du untersuchen möchtest, kannst du bestimmte Elemente priorisieren oder zusätzliche Funktionen hinzufügen."""
