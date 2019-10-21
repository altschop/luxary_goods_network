from selenium import webdriver
import time


class StockXClient:
    def __init__(self):
        self.shoes = []
        self.link = "https://stockx.com/sneakers/top-selling"

    def getShoes(self, numShoes=100):
        browser = webdriver.Chrome(executable_path="./chromedriver.exe")
        browser.maximize_window()
        browser.get(self.link)

        time.sleep(60)

        shoes = browser.find_elements_by_css_selector("tile.browse-tile")
        print(len(shoes))
        for shoe in shoes:
            shoe.click()
            browser.back()

        browser.close()
