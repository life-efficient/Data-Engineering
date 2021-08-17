from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()
URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
driver.get(URL)
cookies_button = driver.find_element_by_xpath('//button[@class="ui-button-primary ui-cookie-accept-all-medium-large"]')
cookies_button.click()
prop_container = driver.find_element_by_xpath('//div[@class="css-kdnpqc-ListingsContainer earci3d2"]')
prop_list = prop_container.find_elements_by_xpath('./div')
num_prop = len(prop_list)
data = {"sale_price": [], "num_bedrooms": [], "sqft": [], "description": [], "address": []}
for i in range(num_prop):
    prop_container = driver.find_element_by_xpath('//div[@class="css-kdnpqc-ListingsContainer earci3d2"]')
    house = prop_container.find_elements_by_xpath('./div')[i]
    house.click()
    time.sleep(5)
    try:
        sale_price = driver.find_element_by_xpath('//span[@data-testid="price"]').text
        data['sale_price'].append(sale_price)
    except NoSuchElementException:
        data['sale_price'].append(None)
    try:
        n_bedrooms = driver.find_element_by_xpath('//span[@data-testid="beds-label"]').text
        data['num_bedrooms'].append(n_bedrooms)
    except NoSuchElementException:
        data['num_bedrooms'].append(None)
    try:
        sqft = driver.find_element_by_xpath('//span[@data-testid="floorarea-label"]').text
        data['sqft'].append(sqft)
    except NoSuchElementException:
        data['sqft'].append(None)
    try:
        div_tag = driver.find_element_by_xpath('//div[@data-testid="truncated_text_container"]')
        span_tag = div_tag.find_element_by_xpath('.//span')
        description = span_tag.text
        data['description'].append(description)
    except NoSuchElementException:
        data['description'].append(None)
    try:
        address = driver.find_element_by_xpath('//span[@data-testid="address-label"]').text
        data['address'].append(address)
    except NoSuchElementException:
        data['address'].append(None)
    driver.back()
    time.sleep(1)