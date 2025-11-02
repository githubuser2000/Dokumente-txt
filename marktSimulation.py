#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-
import random

"""Die Simulation besteht aus zwei Klassen: Market und Participant. Die Market-Klasse enthält eine Liste von Verkäufern und Käufern und eine Methode simulate, die eine bestimmte Anzahl von Iterationen durchführt. In jeder Iteration wird ein zufälliger Verkäufer und ein zufälliger Käufer ausgewählt und ein Preis wird als Durchschnitt ihrer Angebote festgelegt. Der Verkäufer verkauft dann an den Käufer zum festgelegten Preis, wodurch sich ihre Geldbeträge ändern. Der Preis wird auch für jeden Teilnehmer gespeichert, um den intersubjektiven Konsens zu modellieren. Das Ergebnis jeder Iteration wird auf der Konsole ausgegeben.

Die Participant-Klasse enthält den Namen des Teilnehmers, den Geldbetrag und den aktuellen Preis. Die __repr__-Methode wird überschrieben, um eine lesbare Darstellung des Teilnehmers zu erzeugen.

Die Simulation kann mit einer Liste von Verkäufern und Käufern initialisiert werden. In diesem Beispiel haben wir drei Verkäufer und zwei Käufer. Wir führen dann die Simulation für 10 Iterationen aus, indem wir die simulate-Methode der Market-Klasse aufrufen."""


class Market:
    def __init__(self, sellers, buyers):
        self.sellers = sellers
        self.buyers = buyers

    def simulate(self, iterations):
        for i in range(iterations):
            seller = random.choice(self.sellers)
            buyer = random.choice(self.buyers)
            price = (seller.price + buyer.price) / 2
            seller.money += price
            buyer.money -= price
            seller.price = price
            buyer.price = price
            print(
                f"Iteration {i}: {seller.name} sells to {buyer.name} for {price} money units"
            )


class Participant:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.price = random.randint(1, 10)

    def __repr__(self):
        return f"{self.name} ({self.money} money units)"


sellers = [
    Participant("Alice", 100),
    Participant("Bob", 50),
    Participant("Charlie", 75),
]
buyers = [Participant("Dave", 200), Participant("Eve", 150)]

market = Market(sellers, buyers)
market.simulate(10)

"""Natürlich kann ich das! Hier sind einige mögliche Erweiterungen für die Simulation:

+    Angebot und Nachfrage: Statt nur einen Verkäufer und einen Käufer zufällig auszuwählen, können Sie eine Liste von Verkäufern und Käufern nach Angebot und Nachfrage sortieren und dann diejenigen auswählen, die am besten zusammenpassen. Sie können auch die Anzahl der Verkäufer und Käufer sowie deren Preise zufällig variieren, um eine realistischere Simulation zu erhalten.

+    Steuern und Subventionen: Sie können die Simulation um Steuern und Subventionen erweitern, indem Sie beispielsweise eine Steuer auf Verkäufe einführen, die vom Verkäufer gezahlt wird und den Preis erhöht, den der Käufer zahlt. Eine Subvention könnte den umgekehrten Effekt haben, indem sie den Preis senkt, den der Käufer zahlt.

    Externe Faktoren: Sie können externe Faktoren wie Wetterbedingungen, saisonale Nachfrage oder politische Ereignisse einbeziehen, die den Preis und die Nachfrage beeinflussen können.

+    Wettbewerb: Sie können den Markt um Wettbewerb erweitern, indem Sie mehrere Verkäufer und Käufer hinzufügen und sehen, wie sich dies auf den Preis auswirkt. Sie können auch die Simulation so ändern, dass die Teilnehmer ihre Preise basierend auf den Preisen ihrer Konkurrenten anpassen.

+    Spekulation: Sie können die Simulation um Spekulation erweitern, indem Sie Teilnehmer hinzufügen, die nicht beabsichtigen, ein Produkt tatsächlich zu kaufen oder zu verkaufen, sondern nur auf Preisänderungen spekulieren. Diese Teilnehmer könnten beispielsweise versuchen, Produkte zu niedrigen Preisen zu kaufen und zu höheren Preisen zu verkaufen, um Gewinne zu erzielen."""
