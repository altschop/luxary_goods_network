from os import listdir

known_brands = ["adidas", "air jordan", "new balance", "human made", "jordan", "converse", "nike", "vans", "asics",
                "reebok", "puma", "dc", "prada", "gucci"]


def label_brand(query):
    for i in range(len(known_brands)):
        if query.lower().find(known_brands[i]) != -1:
            print(known_brands[i])
            return i

    return -1
