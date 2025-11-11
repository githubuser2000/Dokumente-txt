#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

import random

"""Ja, gerne! Um Spekulation zu unserer Simulation hinzuzufügen, können wir den Teil der Participant-Klasse, der für den Kauf und Verkauf von Produkten verantwortlich ist, erweitern, damit die Teilnehmer auch in der Lage sind, Produkte zu kaufen oder zu verkaufen, ohne sie tatsächlich zu besitzen. Dazu können wir einfach den vorhandenen buy_product()- und sell_product()-Methoden einen quantity-Parameter hinzufügen, der die Anzahl der Produkte angibt, die gekauft oder verkauft werden sollen.

Dann können wir eine neue Methode speculate() in der Participant-Klasse hinzufügen, die es den Teilnehmern ermöglicht, Produkte zu kaufen oder zu verkaufen, ohne sie tatsächlich zu besitzen, indem sie einfach eine Position in dem betreffenden Produkt einnehmen und später zu einem anderen Preis verkaufen. Diese Methode verwendet die vorhandenen buy_product()- und sell_product()-Methoden und führt entsprechende Aktionen aus, um eine Position in einem Produkt zu eröffnen oder zu schließen."""


class Product:
    def __init__(self, name):
        self.name = name


class Event:
    def __init__(self, name, apple_factor, banana_factor, cherry_factor):
        self.name = name
        self.apple_factor = apple_factor
        self.banana_factor = banana_factor
        self.cherry_factor = cherry_factor


class Participant:
    def __init__(self, name, money, product, quantity):
        self.name = name
        self.money = money
        self.positions = {product: quantity}

    def buy_product(self, product, quantity, price):
        cost = price * quantity
        if self.money >= cost:
            self.money -= cost
            if product in self.positions:
                self.positions[product] += quantity
            else:
                self.positions[product] = quantity
            return True
        else:
            return False

    def sell_product(self, product, quantity, price):
        if product in self.positions and self.positions[product] >= quantity:
            revenue = price * quantity
            self.money += revenue
            self.positions[product] -= quantity
            return True
        else:
            return False

    def speculate(self, product, quantity, price):
        if random.choice([True, False]):
            return self.buy_product(product, quantity, price)
        else:
            return self.sell_product(product, quantity, price)


class Market:
    def __init__(self, sellers, buyers, products, events):
        self.sellers = sellers
        self.buyers = buyers
        self.products = products
        self.events = events
        self.prices = {product: 1 for product in products}

    def update_price(self, product, price):
        self.prices[product] = price

    def get_price(self, product):
        return self.prices[product]

    def simulate(self, periods):
        for i in range(periods):
            for event in self.events:
                if random.choice([True, False]):
                    for product in self.products:
                        self.update_price(
                            product, self.get_price(product) * event.apple_factor
                        )
                else:
                    for product in self.products:
                        self.update_price(
                            product, self.get_price(product) * event.banana_factor
                        )
            for participant in random.sample(
                self.sellers + self.buyers, len(self.sellers + self.buyers)
            ):
                product = participant.positions
                for p in product:
                    price = self.get_price(p)
                    quantity = random.randint(1, 5)
                    if random.choice([True, False]):
                        participant.speculate(p, quantity, price)
                    else:
                        if isinstance(participant, Buyer):
                            sellers = self.sellers
                        else:
                            sellers = [b for b in self.buyers if b != participant]
                        random_seller = random.choice(sellers)
                        random_seller.speculate(p, quantity, price)

# Beispielprogramm
# Erstellen von Verkäufern, Käufern und Produkten
sellers = [Participant("Seller1", "seller") for i in range(3)]
buyers = [Participant("Buyer1", "buyer") for i in range(3)]
products = [Product("Apple"), Product("Banana"), Product("Cherry")]

# Erstellen von Markt-Events
event1 = MarketEvent(1.5, 1, 1)
event2 = MarketEvent(1, 1.5, 1)

# Erstellen des Markts
market = Market(sellers, buyers, products, [event1, event2])

# Simulation des Markts für 3 Perioden
market.simulate(3)

# Ausgabe der Positionen der Teilnehmer
for participant in sellers + buyers:
    print(participant.name, ":", participant.positions)

# Ausgabe der Preise
for product in products:
    print(product.name, ":", market.get_price(product))
