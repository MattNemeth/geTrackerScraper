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
        #print("Current item price: ", end='')
        #print(item_sell_price[0].text)

        return item_current_price[0].text
    def extract_item_min_price(self):
        item_buy_price = self.driver.find_elements_by_id("item_stat_sell_price")
        #print("Item buy price: ", end='')
        #print(item_buy_price[0].text)

        return item_buy_price[0].text
    def extract_item_max_price(self):
        item_sell_price = self.driver.find_elements_by_id("item_stat_offer_price")
        #print("Item sell price: ", end='')
        #print(item_sell_price[0].text)

        return item_sell_price[0].text

    # def test(self):
    #     print("URL for item: ", end='')
    #     print(osrs_item)
    #     print(self.url)

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

#scraper.test()

for i in range(len(osrs_items)):
    scraper = geTrackerScraper(osrs_items[i])
    scraper.loadGETrackerURL()
    currentPrices.append(scraper.extract_item_current_price())
    buyPrices.append(scraper.extract_item_min_price())
    sellPrices.append(scraper.extract_item_max_price())


outSheet.write("A1", "Item")
outSheet.write("B1", "Current Price")
outSheet.write("C1", "Buy Price")
outSheet.write("D1", "Sell Price")
outSheet.write("E1", "Margin")

for j in range(len(osrs_items)):
    for k in range(3):
        #write(row, column, data)
        outSheet.write(j+1, 0, osrs_items[j])
        outSheet.write(j+1, k+1, currentPrices[j])
        outSheet.write(j+1, k+1, buyPrices[j])
        outSheet.write(j+1, k+1, sellPrices[j])
        #outSheet.write(j+1, k+1, (sellPrices[j] - buyPrices[j]))




outWorkbook.close()


# content = driver.page_source
# soup = BeautifulSoup(content)
# for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
# name=a.find('div', attrs={'class':'_3wU53n'})
# price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
# rating=a.find('div', attrs={'class':'hGSR34 _2beYZw'})
# products.append(name.text)
# prices.append(price.text)
# ratings.append(rating.text) 






