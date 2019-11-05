from os import listdir

known_brands = ["adidas", "air jordan", "new balance", "human made", "jordan", "converse", "nike", "vans", "asics",
                "reebok", "puma", "dc", "prada", "gucci", "atmos", "black friday", "footshop", "lebron",
                "kids yeezy", "kobe", "kyrie", "under armour", "zoom kd", "kangaroos"]


def label_brand(query):
    for i in range(len(known_brands)):
        if query.lower().find(known_brands[i]) != -1:
            return i

    return -1
