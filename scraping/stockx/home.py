import requests
from bs4 import BeautifulSoup
import string
import numpy as np
from models.watch import Watch

stockx_watch_home = "https://stockx.com/watches"
num_watch_pages = 25


def getName(result):
    name_scraped = result.find('div', class_='PrimaryText-sc-12c6bzb-0 gMymmc')
    if len(name_scraped.contents) == 0:
        return ""
    elif len(name_scraped.contents) == 1:
        return name_scraped.contents[0]

    title_one = str(name_scraped.contents[0])[5:-6]
    title_two = str(name_scraped.contents[1])[5:-6]
    return title_one + " " + title_two


def getLowestAsk(result):
    ask_scraped = result.find('div', class_='PrimaryText-sc-12c6bzb-0 jwzdVc')
    if len(ask_scraped.contents) == 0:
        return None

    ask = str(ask_scraped.contents[0])
    if ask == '--':
        ask = -1
    else:
        digits = '0123456789'
        table = str.maketrans({key: None for key in string.punctuation})
        # removes commas or other punctuation
        ask = ask[1:len(ask)].translate(table)

    return ask


def getWatchObjects(parsed_content):
    soup = BeautifulSoup(parsed_content, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'tile browse-tile'})
    # print(results)

    watches = []
    for result in results:
        name = getName(result)
        watch = Watch(name, name.split(" ")[0], getLowestAsk(result), 'USD')
        print(watch)
        watches.append(watch)

    return watches


def scrapeHome():
    # needed to bypass security against parsing
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

    watch_objects = []
    page_num = 1
    while page_num <= num_watch_pages:
        parsed_content = requests.get(stockx_watch_home + "?page=" + str(page_num), headers=headers).text
        watch_objects += getWatchObjects(parsed_content)
        page_num += 1

    return watch_objects


def main():
    watch_objects = scrapeHome()


if __name__ == '__main__':
    main()
