#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

"""    Angebot und Nachfrage: Statt nur einen Verkäufer und einen Käufer zufällig auszuwählen, können Sie eine Liste von Verkäufern und Käufern nach Angebot und Nachfrage sortieren und dann diejenigen auswählen, die am besten zusammenpassen. Sie können auch die Anzahl der Verkäufer und Käufer sowie deren Preise zufällig variieren, um eine realistischere Simulation zu erhalten.

    Steuern und Subventionen: Sie können die Simulation um Steuern und Subventionen erweitern, indem Sie beispielsweise eine Steuer auf Verkäufe einführen, die vom Verkäufer gezahlt wird und den Preis erhöht, den der Käufer zahlt. Eine Subvention könnte den umgekehrten Effekt haben, indem sie den Preis senkt, den der Käufer zahlt.

    Externe Faktoren: Sie können externe Faktoren wie Wetterbedingungen, saisonale Nachfrage oder politische Ereignisse einbeziehen, die den Preis und die Nachfrage beeinflussen können.

    Wettbewerb: Sie können den Markt um Wettbewerb erweitern, indem Sie mehrere Verkäufer und Käufer hinzufügen und sehen, wie sich dies auf den Preis auswirkt. Sie können auch die Simulation so ändern, dass die Teilnehmer ihre Preise basierend auf den Preisen ihrer Konkurrenten anpassen.

    Spekulation: Sie können die Simulation um Spekulation erweitern, indem Sie Teilnehmer hinzufügen, die nicht beabsichtigen, ein Produkt tatsächlich zu kaufen oder zu verkaufen, sondern nur auf Preisänderungen spekulieren. Diese Teilnehmer könnten beispielsweise versuchen, Produkte zu niedrigen Preisen zu kaufen und zu höheren Preisen zu verkaufen, um Gewinne zu erzielen."""

"""füge nun Wettbewerb hinzu, wovon du geredet hattest"""

"""Diese Simulation führt nun Wettbewerb ein, indem die Verkäufer und Käufer in zufälliger Reihenfolge ihre Transaktionen durchführen können. Wenn ein Verkäufer oder Käufer einen besseren Preis als den aktuellen Marktpreis anbietet, wird der Preis entsprechend angepasst. Beachte, dass es noch viele Möglichkeiten gibt, diese Simulation weiter auszubauen und zu verbessern, abhängig von den spezifischen Anforderungen und Zielen."""


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
                random.shuffle(sellers)
                random.shuffle(buyers)
                price = None
                for seller in sellers:
                    if supply <= 0:
                        break
                    if price is None or seller.price < price:
                        price = seller.price
                    if seller.price < price:
                        price = seller.price
                    if seller.price < price * event.price_multiplier:
                        price = seller.price
                    if seller.price < max([buyer.price for buyer in buyers], default=0):
                        price = seller.price
                    if price < seller.price:
                        break
                    supply -= 1
                    seller.money += price
                    seller.price = price
                    print(f"{seller.name} sells {product.name} for {price} money units")
                for buyer in buyers:
                    if demand <= 0:
                        break
                    if price is None or buyer.price > price:
                        price = buyer.price
                    if buyer.price > price:
                        price = buyer.price
                    if buyer.price > price * event.price_multiplier:
                        price = buyer.price
                    if buyer.price > min(
                        [seller.price for seller in sellers], default=float("inf")
                    ):
                        price = buyer.price
                    if price > buyer.price:
                        break
                    demand -= 1
                    buyer.money -= price
                    buyer.price = price
                    print(f"{buyer.name} buys {product.name} for {price} money units")


class Participant:
    def __init__(self, name, money, product, price):
        self.name = name
        self.money = money
        self.product = product
        self.price = price

    def __repr__(self):
        return f"{self.name} ({self.money} money units, {self.price} per {self.product.name})"


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
    Event("Harvest", 0.8, 1.5, 1.2),
]

sellers = [
    Participant("Alice", 100, products[0], 1),
    Participant("Bob", 100, products[1], 2),
    Participant("Charlie", 100, products[2], 3),
]

buyers = [
    Participant("Dave", 100, products[0], 5),
    Participant("Eve", 100, products[1], 4),
    Participant("Frank", 100, products[2], 3),
]

market = Market(sellers, buyers, products, events)
market.simulate(10)
