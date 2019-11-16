from os import listdir

known_brands = ["adidas", "new balance", "converse", "nike", "vans", "asics",
                "reebok", "puma", "dc", "prada", "gucci", "atmos", "black friday", "footshop",
                "under armour", "kangaroos"]


def label_brand(query):
    q = query.lower()

    if q.find("jordan") != -1 or q.find("kobe") != -1 or q.find("kyrie") != -1 or q.find("lebron") != -1 \
            or q.find("zoom kd") != -1:
        return known_brands.index("nike")

    if q.find("yeezy") != -1 or q.find("human made") != -1:
        return known_brands.index("adidas")

    for i in range(len(known_brands)):
        if q.find(known_brands[i]) != -1:
            return i

    return -1
