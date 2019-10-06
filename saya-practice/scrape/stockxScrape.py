import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def stockx():
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path='/Users/jsaya01/lg/luxary_goods_network/saya-practice/scrape/chromedriver',
                               chrome_options = option)
    browser.get("https://stockx.com")

    # Wait 20 seconds for page to load
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrap"]/div[1]/div/div[2]')))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    searchField = browser.find_element(By.XPATH, '//*[@id="home-search"]')
    searchField.send_keys("16610")
    time.sleep(10)
    searchField.send_keys(Keys.ENTER)


    browser.quit()

if __name__ == '__main__':
    stockx()