#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

"""    Angebot und Nachfrage: Statt nur einen Verkäufer und einen Käufer zufällig auszuwählen, können Sie eine Liste von Verkäufern und Käufern nach Angebot und Nachfrage sortieren und dann diejenigen auswählen, die am besten zusammenpassen. Sie können auch die Anzahl der Verkäufer und Käufer sowie deren Preise zufällig variieren, um eine realistischere Simulation zu erhalten.

    Steuern und Subventionen: Sie können die Simulation um Steuern und Subventionen erweitern, indem Sie beispielsweise eine Steuer auf Verkäufe einführen, die vom Verkäufer gezahlt wird und den Preis erhöht, den der Käufer zahlt. Eine Subvention könnte den umgekehrten Effekt haben, indem sie den Preis senkt, den der Käufer zahlt.

    Externe Faktoren: Sie können externe Faktoren wie Wetterbedingungen, saisonale Nachfrage oder politische Ereignisse einbeziehen, die den Preis und die Nachfrage beeinflussen können.

    Wettbewerb: Sie können den Markt um Wettbewerb erweitern, indem Sie mehrere Verkäufer und Käufer hinzufügen und sehen, wie sich dies auf den Preis auswirkt. Sie können auch die Simulation so ändern, dass die Teilnehmer ihre Preise basierend auf den Preisen ihrer Konkurrenten anpassen.

    Spekulation: Sie können die Simulation um Spekulation erweitern, indem Sie Teilnehmer hinzufügen, die nicht beabsichtigen, ein Produkt tatsächlich zu kaufen oder zu verkaufen, sondern nur auf Preisänderungen spekulieren. Diese Teilnehmer könnten beispielsweise versuchen, Produkte zu niedrigen Preisen zu kaufen und zu höheren Preisen zu verkaufen, um Gewinne zu erzielen."""


"""Kannst du vielleicht einen dieser Punkte dazu programmieren?"""


"""Die Simulation besteht aus zwei Klassen: Market und Participant. Die Market-Klasse enthält eine Liste von Verkäufern und Käufern und eine Methode simulate, die eine bestimmte Anzahl von Iterationen durchführt. In jeder Iteration wird ein zufälliger Verkäufer und ein zufälliger Käufer ausgewählt und ein Preis wird als Durchschnitt ihrer Angebote festgelegt. Der Verkäufer verkauft dann an den Käufer zum festgelegten Preis, wodurch sich ihre Geldbeträge ändern. Der Preis wird auch für jeden Teilnehmer gespeichert, um den intersubjektiven Konsens zu modellieren. Das Ergebnis jeder Iteration wird auf der Konsole ausgegeben.

Die Participant-Klasse enthält den Namen des Teilnehmers, den Geldbetrag und den aktuellen Preis. Die __repr__-Methode wird überschrieben, um eine lesbare Darstellung des Teilnehmers zu erzeugen.

Die Simulation kann mit einer Liste von Verkäufern und Käufern initialisiert werden. In diesem Beispiel haben wir drei Verkäufer und zwei Käufer. Wir führen dann die Simulation für 10 Iterationen aus, indem wir die simulate-Methode der Market-Klasse aufrufen."""

"""Ja, gerne! Hier ist eine Erweiterung der Simulation mit externen Faktoren. Wir werden eine Liste von Produkten erstellen, die von Verkäufern angeboten werden, und eine Liste von Ereignissen, die den Preis und die Nachfrage dieser Produkte beeinflussen können."""


import random


class Market:
    def __init__(self, sellers, buyers, products, events):
        self.sellers = sellers
        self.buyers = buyers
        self.products = products
        self.events = events

    def simulate(self, iterations):
        for i in range(iterations):
            event = random.choice(self.events)
            print(f"\nIteration {i+1}: {event}")
            for product in self.products:
                sellers = [
                    seller for seller in self.sellers if seller.product == product
                ]
                buyers = [buyer for buyer in self.buyers if buyer.product == product]
                demand = random.randint(1, 10) * event.demand_multiplier
                supply = random.randint(1, 10) * event.supply_multiplier
                for j in range(min(len(sellers), supply)):
                    seller = random.choice(sellers)
                    price = seller.price * event.price_multiplier
                    buyer = random.choice(buyers)
                    seller.money += price
                    buyer.money -= price
                    seller.price = price
                    buyer.price = price
                    print(
                        f"{seller.name} sells {product.name} to {buyer.name} for {price} money units"
                    )


class Participant:
    def __init__(self, name, money, product, price):
        self.name = name
        self.money = money
        self.product = product
        self.price = price

    def __repr__(self):
        return f"{self.name} ({self.money} money units)"


class Product:
    def __init__(self, name):
        self.name = name


class Event:
    def __init__(self, name, price_multiplier, demand_multiplier, supply_multiplier):
        self.name = name
        self.price_multiplier = price_multiplier
        self.demand_multiplier = demand_multiplier
        self.supply_multiplier = supply_multiplier


products = [Product("Apple"), Product("Banana"), Product("Cherry")]
events = [
    Event("Normal", 1, 1, 1),
    Event("Drought", 1.5, 0.5, 0.8),
    Event("Harvest", 0.8, 1.2, 1.5),
    Event("War", 2, 0.2, 0.2),
]

sellers = [
    Participant("Alice", 100, products[0], 5),
    Participant("Bob", 50, products[1], 3),
    Participant("Charlie", 75, products[2], 2),
]

buyers = [
    Participant("Dave", 200, products[0], 0),
    Participant("Eve", 150, products[1], 0),
    Participant("Frank", 80, products[2], 0),
]

market = Market(sellers, buyers, products, events)
market.simulate(5)
