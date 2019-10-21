import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import urllib3
import urllib.request
import shutil
import base64
from google_images_download import google_images_download
import io
import requests
import time
import os


class GoogleScraper:
    def __init__(self):
        self.link = "https://www.google.com/imghp?hl=en"

    def download_images(self, query, elements, count):
        for cnt in range(count):
            path = os.getcwd() + "/" + query
            try:
                os.mkdir(path)
            except OSError:
                print("Path exists")

            src = elements[cnt].get_attribute('src')
            filename = query + str(cnt) + ".jpg"
            urllib.request.urlretrieve(src, filename)

            try:
                img = Image.open(filename)
                img.verify()  # I perform also verify, don't know if he sees other types o defects

                img = Image.open(filename)
                img.resize((90, 150))
                img.save(filename)
                img.close()  # reload is necessary in my case
                shutil.move("./" + filename, "./" + query + "/" + filename)
            except OSError:
                print("removing")
                os.remove(filename)

    def scrape_images(self, queries, countPerQuery=5):
        if len(queries) < 1:
            return None

        browser = webdriver.Chrome(executable_path="../chromedriver.exe")
        browser.maximize_window()
        browser.get(self.link)

        input = browser.find_element_by_xpath("//*[@id=\"sbtc\"]/div/div[2]/input")
        # type query, then press enter
        input.send_keys(queries[0])
        input.send_keys(Keys.ENTER)

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

        # get the image source
        # img = driver.find_element_by_xpath('//div[@id="recaptcha_image"]/img')
        # src = img.get_attribute('src')

        # download the image
        # urllib.urlretrieve(src, "captcha.png")

        # driver.close()


# response = google_images_download.googleimagesdownload()
# arguments = {"keywords": "test",
# "format": "jpg",
# "limit": 4,
# "print_urls": True,
# "size": "medium",
# "aspect_ratio": "panoramic"}

# response.download(arguments)

scraper = GoogleScraper()
scraper.scrape_images(["dollar"])
