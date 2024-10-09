from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# %%

def reParse(phrase):
    results = re.findall("\d+(?:\.\d+)?", phrase)
    return results

# %%

def print_info(retailer, list_price="n/a", percent_off="n/a", current_price="n/a", stock="n/a", img="n/a"):
    print("Retailer:", retailer)
    print("Listing price:", list_price)
    print("Percent off:", percent_off)
    print("Current price:", current_price)
    print("Availability:", stock)
    print("Image link:", img)

# %%

def scrape_amazon(id):
    retailer = 'Amazon'

    # initialize the driver
    service = Service('')
    options = Options()
    options.add_argument('headless') # -- disable these for debugging
    options.add_argument('disable-gpu') # disable these for debugging
    driver = webdriver.Edge(service=service, options=options, keep_alive=False)

    # navigate to page
    driver.get("https://amazon.com")

    # locate the search box, input the query, select the first result
    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
    search_box.send_keys("Lego " + id)
    driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, id).click()

    # get the item's picture, listing price, current price, percentage off, and availability
    img = driver.find_element(By.XPATH, '//*[@id="landingImage"]').get_attribute('src') # gets image
    pricing_info = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]').get_attribute('innerText') # gets current price and the percentage off
    list_phrase = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[1]').get_attribute('innerText') # gets listing price
    pricing_info = reParse(pricing_info) # filters unnecessary information
    list_price = reParse(list_phrase) # filters unnecessary information
    stock = driver.find_element(By.XPATH, '//*[@id="availability"]/span').get_attribute('innerText')

    # format the listing price, current price, and percentage off
    list_price = list_price[0]
    list_price = float(list_price)
    current_price = pricing_info[0]
    current_price = float(current_price)
    percent_off = pricing_info[1]
    percent_off = int(percent_off)

    # print the scraped information to the terminal
    print_info(retailer, list_price, percent_off, current_price, stock, img)

    driver.close()

# %%

def scrape_ebay(id):
    retailer = 'eBay'

    # initialize the driver
    service = Service('')
    options = Options()
    options.add_argument('headless') # -- disable these for debugging
    options.add_argument('disable-gpu') # disable these for debugging
    driver = webdriver.Edge(service=service, options=options, keep_alive=False)

    # navigate to page
    driver.get("https://ebay.com")

    # locate the search box, input the query, select the first result
    search_box = driver.find_element(By.XPATH, '//*[@id="gh-ac"]')
    search_box.send_keys("Lego " + id)
    driver.find_element(By.XPATH, '//*[@id="gh-btn"]').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, id).click()

    # get the item's picture, listing price, current price, and percentage off
    img = driver.find_element(By.XPATH, '//*[@id="PicturePanel"]/div/div/div[1]/div[1]/div[1]/div[4]/div[1]/img').get_attribute('src') # gets image
    # aok_phrase = web_page.find_element(By.XPATH, '').get_attribute('innerText') # gets current price and the percentage off     # UNSURE IF THESE ARE NEEDED HERE,
    # pricing_info = re.findall("\d+(?:\.\d+)?", aok_phrase) # filters unnecessary information                                    # FURTHER TESTING IS REQUIRED.
    list_phrase = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/div[1]/div/div/div/div[1]/span').get_attribute('innerText') # gets listing price
    list_price = re.findall("\d+(?:\.\d+)?", list_phrase) # filters unnecessary information

    # format the listing price, current price, and percentage off
    list_price = list_price[0]
    list_price = float(list_price)
    # current_price = pricing_info[0]
    # current_price = float(current_price)
    # percent_off = pricing_info[1]
    # percent_off = int(percent_off)

    # print the scraped information to the terminal
    # print_info(retailer, list_price, percent_off, current_price, stock, img)

    driver.close()

# %%

'''
NOTES:
• Add WebDriverWait to prevent a failed scrape - NoSuchElementFound Exception.
--- https://stackoverflow.com/questions/72657844/python-selenium-nosuchelementexception-although-the-value-was-found

• Add other scrapers here
• Insert element logic - if no discount found, list_price = current_price (something like that)




LAST WORKED ON:
• Added Expected Conditions and WebDriverWait to scrape_amazon(), added a Try/Except as a method of catching a listing without multiple prices (listing & current)
• Try/Except is currently culprit of crashes, must iron this out.
'''
# %%
