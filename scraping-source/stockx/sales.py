import requests
from bs4 import BeautifulSoup
from models.sale import Sale
import utils
import datetime
import json
from selenium import webdriver


class WatchLink:
    def __init__(self, brand, model, version, link):
        self.brand = brand
        self.model = model
        self.version = version
        self.link = link
        self.currency = utils.CURRENCY_USD

    def __str__(self):
        return "Watch Brand: " + self.brand + " Model: " + self.model + \
               " Version: " + str(self.version) + " Link: " + str(self.link) + \
               " Currency: " + self.currency


watches = [WatchLink(utils.BRAND_ROLEX, utils.MODEL_DATEJUST, utils.VERSION_16013,
                     utils.LINK_DATEJUST_16013),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_YACHT_MASTER_TWO, utils.VERSION_BLUE_116680,
                     utils.LINK_YACHT_MASTER_BLUE),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_GMT_MASTER_TWO, utils.VERSION_116710BLNR,
                     utils.LINK_GMT_MASTER_116710BLNR),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_SUBMARINER, utils.VERSION_114060,
                     utils.LINK_SUBMARINER_114060),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_SUBMARINER, utils.VERSION_16610,
                     utils.LINK_SUBMARINER_16610),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_GMT_MASTER_TWO, utils.VERSION_116710LN,
                     utils.LINK_GMT_MASTER_116710LN),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_SUBMARINER, utils.VERSION_116610LV,
                     utils.LINK_SUBMARINER_116610LV),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_GMT_MASTER_TWO, utils.VERSION_126711CHNR,
                     utils.LINK_GMT_MASTER_126711CHNR),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_DATEJUST, utils.VERSION_DIAMOND_16013,
                     utils.LINK_DATEJUST_DIAMOND_DIAL_16013),
           WatchLink(utils.BRAND_ROLEX, utils.MODEL_SUBMARINER, utils.VERSION_16613,
                     utils.LINK_SUBMARINER_16613),
           ]


def getDateAndPrice(response):
    return {"date": response["createdAt"], "price": response["amount"]}


def retrieveSales(watches):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }
    sales = []

    for watch in watches:
        response = json.loads(requests.get(watch.link, headers=headers).text)
        print(watch)
        print(response)

        count = 0
        for sale in response:
            temp = Sale(watch.brand, watch.model, watch.version, sale["amount"],
                        sale["createdAt"], utils.CURRENCY_USD)
            print(temp)
            sales.append(temp)
            count += 1
        print(str(count))

    return sales


def selScrape():
    link = "https://stockx.com/search/watches?s=rolex"
    browser = webdriver.Chrome(executable_path="./chromedriver.exe")
    browser.get(link)

    for watch in browser.find_elements_by_class_name("browse-tile"):
        print(watch)


def main():
    selScrape()
    # sales = retrieveSales(watches)
    # print(len(sales))


main()
