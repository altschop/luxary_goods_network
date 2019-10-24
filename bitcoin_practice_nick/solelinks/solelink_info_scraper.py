from selenium import webdriver
import string
from solelinks.solelink_info import ShoeInfo


class ShoeInfoScraper:
    def __init__(self):
        self.shoes = []

    def getShoeInfos(self, num_shoes):
        browser = webdriver.Chrome(executable_path="./chromedriver.exe")
        browser.maximize_window()

        browser.get("https://solelinks.com/")
        browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[1]/div[2]/div[1]/ul/li[2]").click()

        shoe_infos = []
        found = browser.find_elements_by_class_name("col-3")
        while len(found) > 0 and len(shoe_infos) < num_shoes:
            for shoe in found:
                if len(shoe_infos) >= num_shoes:
                    browser.close()
                    return shoe_infos

                contents = shoe.text.split("\n")
                # strips punctuation off of shoe name
                name = contents[0].translate(str.maketrans('', '', string.punctuation))
                shoe_info = ShoeInfo(name.rstrip(), contents[1])
                shoe_infos.append(shoe_info)
                print(shoe_info.name)

                if shoe_info.name == "Nike Air VaporMax 97 Japan" and shoe_info.release_date == "03-09-2018":
                    browser.close()
                    return shoe_infos

            btns = browser.find_elements_by_css_selector(".page-link.button.hoverable")
            if len(btns) == 1 and btns[0].text == "Previous":
                break

            for btn in btns:
                if btn.text == "Next":
                    btn.click()
                    break

            found = browser.find_elements_by_class_name("col-3")

        browser.close()
        return shoe_infos
