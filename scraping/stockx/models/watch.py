from collections import namedtuple


class Watch:
    def __init__(self, name, brand, lowest_ask, currency):
        self.name = name
        self.brand = brand
        self.lowest_ask = lowest_ask
        self.currency = currency

    def __str__(self):
        return "Watch Name: " + self.name + " Brand: " + self.brand + \
               " Lowest Ask: " + str(self.lowest_ask) + " Currency: " + self.currency


WatchTuple = namedtuple('WatchTuple', 'name brand lowest_ask currency')
