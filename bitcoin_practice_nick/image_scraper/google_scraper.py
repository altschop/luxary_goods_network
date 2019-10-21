import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import urllib.request
import shutil
import os
from os import listdir
import random


class GoogleScraper:
    def __init__(self, trainPerent=0.2):
        self.link = "https://www.google.com/imghp?hl=en"
        self.trainPercent = trainPerent

    def move_random_images_to_test(self, query, train_path):
        # randomly pick some of them and move them to testing data
        test_path = os.getcwd() + "/test_data/" + query
        try:
            os.mkdir(test_path)
        except OSError:
            print()  # do nothing

        try:
            filenames = listdir(train_path).copy()
        except FileNotFoundError:
            return

        numToPick = int(len(filenames) * self.trainPercent)
        random.shuffle(filenames)
        numPicked = 0

        while numPicked < numToPick:
            name = filenames[numPicked]
            shutil.move("./train_data/" + query + "/" + name, "./test_data/" + query + "/" + name)
            numPicked += 1

    def download_images(self, query, elements, count):
        print(query)
        train_path = os.getcwd() + "/train_data/" + query
        try:
            os.mkdir(train_path)
        except OSError:
            print()  # do nothing

        for cnt in range(count):
            if cnt >= len(elements):
                return

            src = elements[cnt].get_attribute('src')
            if src is None:
                continue
            filename = query + "_" + str(cnt) + ".jpg"
            urllib.request.urlretrieve(src, filename)

            try:
                img = Image.open(filename)
                img.verify()  # I perform also verify, don't know if he sees other types o defects

                img = Image.open(filename)
                img.save(filename)
                img.close()  # reload is necessary in my case
                shutil.move("./" + filename, "./train_data/" + query + "/" + filename)
            except OSError:
                os.remove(filename)

        self.move_random_images_to_test(query, train_path)

    def scrape_images(self, queries, countPerQuery=100):
        if len(queries) < 1:
            return None

        browser = webdriver.Chrome(executable_path="./chromedriver.exe")
        browser.maximize_window()
        browser.get(self.link)

        search = browser.find_element_by_xpath("//*[@id=\"sbtc\"]/div/div[2]/input")
        # type query, then press enter
        search.send_keys(queries[0])
        search.send_keys(Keys.ENTER)

        numQuery = 0
        while numQuery < len(queries):
            imgs = browser.find_elements_by_tag_name("img")
            print(len(imgs))
            self.download_images(queries[numQuery], imgs, countPerQuery)

            try:
                nextSearch = browser.find_element_by_xpath("//*[@id=\"sbtc\"]/div/div[2]/input")
            except NoSuchElementException:
                break

            numQuery += 1
            if numQuery == len(queries):
                break

            nextSearch.clear()
            nextSearch.send_keys(queries[numQuery])
            nextSearch.send_keys(Keys.ENTER)

        browser.close()