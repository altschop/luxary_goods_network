import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scrapeSimple():
    page = requests.get('https://www.ebay.com/b/Rolex-Wristwatches/31387/bn_2989578')
    soup = BeautifulSoup(page.text, 'html.parser')
    lis = soup.select('#w8-xCarousel-x-carousel')[0].find('ul').find_all('li')
    for li in lis:
        info = li.select('.b-info')[0]
        name = info.select('.b-info__title')[0].text
        price = info.select('.b-info__price.clearfix')[0].find('span').text
        result = '{:<80}: {}'.format(name, str(price))
        print(result)

def scrapeAllPages():
    baseUrl = 'https://www.ebay.com/b/Rolex-Wristwatches/31387/bn_2989578?LH_AV=1&rt=nc&_pgn'
    pageNumber = 1
    watches = []
    while(True):
        try:
            page = requests.get('{}={}'.format(baseUrl, pageNumber))
            soup = BeautifulSoup(page.text, 'html.parser')
            listElems = soup.find(id='mainContent').find(id='w7').select('ul')[-1].find_all('li')
            for li in listElems:
                name = li.find('h3').text
                price = li.find(class_='s-item__price').text
                watch = '{}: {:<80}: {}'.format(len(watches), name, price)
                watches.append(watch)
            print("Finished page {}, Loaded {} Watches".format(str(pageNumber), str(len(watches))))
            pageNumber += 1
        except:
            break
    for watch in watches:
        print(watch)


if __name__ == '__main__':
    scrapeAllPages()

def seleniumExampleUseage():
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
