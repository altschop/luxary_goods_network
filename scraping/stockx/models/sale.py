
import datetime
from operator import attrgetter

class Sale:
    def __init__(self, brand, model, version, price, date, currency):
        self.brand = brand
        self.model = model
        self.version = version
        self.price = price
        self.date = date.split('T')[0]
        self.datetime = datetime.datetime.fromisoformat(date)
        self.currency = currency

    def __str__(self):
        return "Watch Brand: " + self.brand + " Model: " + self.model + \
               " Version: " + str(self.version) + " Price: " + str(self.price) + \
               " Currency: " + self.currency

    def getInformation(self, attrs):
        getters = [attrgetter(attr.lower()) for attr in attrs]
        return [getter(self) for getter in getters]

