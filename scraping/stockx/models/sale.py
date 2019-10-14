class Sale:
    def __init__(self, brand, model, version, price, date, currency):
        self.brand = brand
        self.model = model
        self.version = version
        self.price = price
        self.date = date
        self.currency = currency

    def __str__(self):
        return "Watch Brand: " + self.brand + " Model: " + self.model + \
               " Version: " + str(self.version) + " Price: " + str(self.price) + \
               " Currency: " + self.currency
