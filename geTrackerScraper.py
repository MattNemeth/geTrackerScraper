#Web Scraper that will look at osrs ge tracker and get margins of items I like to flip
#print('This will be my GE Tracker Web Scraper using Python 3.7')

import xlsxwriter

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request

#import pandas as pd


#need to check the file path
# driver = webdriver.Chrome(executable_path=r"C:\Users\nemet\Downloads\chromedriver_win32")
# driver.get("https://www.ge-tracker.com/item/zulrah-s-scales")

class geTrackerScraper(object):
    def __init__(self, osrs_items):
        self.osrs_items = osrs_items

        #we create the url by the parameters passed in. 
        self.url = f"https://www.ge-tracker.com/item/{osrs_items}"

        self.driver = webdriver.Chrome("C:/Users/nemet/Downloads/chromedriver_win32/chromedriver.exe")
        self.delay = 1

    def loadGETrackerURL(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #inspecting the GE Tracker site, item price is labeled as ID "item_stat_overall"
            wait.until(EC.presence_of_element_located((By.ID, "item_stat_overall")))
            print("Page is Ready")
        except TimeoutException:
            print("Page took too long to load")

    def extract_item_current_price(self):
        item_current_price = self.driver.find_elements_by_id("item_stat_overall")
        return item_current_price[0].text
    def extract_item_min_price(self):
        item_buy_price = self.driver.find_elements_by_id("item_stat_sell_price")
        return item_buy_price[0].text
    def extract_item_max_price(self):
        item_sell_price = self.driver.find_elements_by_id("item_stat_offer_price")
        return item_sell_price[0].text

#create file (workbook) and worksheet
outWorkbook = xlsxwriter.Workbook("osrsItems.xlsx")
outSheet = outWorkbook.add_worksheet()

osrs_items = ["zulrah-s-scales", 
              "blood-rune", 
              "grimy-toadflax",
              "mist-rune",
              "revenant-ether"]

currentPrices = []
buyPrices = []
sellPrices = []
#margins = []


for i, item in enumerate(osrs_items):
        scraper = geTrackerScraper(osrs_items[i])
        scraper.loadGETrackerURL()
        currentPrices.append(scraper.extract_item_current_price())
        buyPrices.append(scraper.extract_item_min_price())
        sellPrices.append(scraper.extract_item_max_price())

for j, item in enumerate(osrs_items):
    for k in range(3):
            outSheet.write(0, 0, "Item")
            outSheet.write(0, 1, "Current Price")
            outSheet.write(0, 2, "Buy Price")
            outSheet.write(0, 3, "Sell Price")
            #i might just be dumb/unfamiliar with python but can't figure out
            #a nicer way to print to the excel sheet. This for loop feels... odd
            
            #write(row, column, data)
            outSheet.write(j+1, 0, item)
            outSheet.write(j+1, k+1, currentPrices[j])
            outSheet.write(j+1, k+1, buyPrices[j])
            outSheet.write(j+1, k+1, sellPrices[j])

outWorkbook.close()
