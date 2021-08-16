from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from tqdm import tqdm
import json
import re
import time
from bs4 import BeautifulSoup
import random
import string

def infinite_scroll(driver):
    # Scroll until no more challenges appear
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def look_and_click(driver, by, label):
    while True:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, label))
            )
            button.click()
        except StaleElementReferenceException:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, label))
            )
        else:
            break
    return button

USERNAME ='' ### Your Username
PASSWORD ='' ### Your password

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome('chrome_driver/chromedriver') 
driver.get("https://www.hackerrank.com/login?h_r=login&h_l=body_middle_left_button")

user_button = look_and_click(driver, By.ID, 'input-1')
user_button.send_keys(USERNAME)

time.sleep(1)

password_button = look_and_click(driver, By.ID, 'input-2')
password_button.send_keys(PASSWORD)

time.sleep(1)

password_button = look_and_click(driver, By.XPATH,
                                 '//*[@id="tab-1-content-1"]/div[1]/form' + \
                                 '/div[4]/button/div/span')

time.sleep(1)
python_button = look_and_click(driver, By.XPATH,
                               '//div[@data-automation="python"]')

infinite_scroll(driver)
time.sleep(1)
HTML = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
soup = BeautifulSoup(HTML, 'lxml')
challenge_table = soup.find("div", {"class": "challenges-list"})
challenge_list = challenge_table.find_all('a', {'class': 'js-track-click challenge-list-item'})
challenges_dict = {''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(8)) + '.yaml':{} for _ in challenge_list}
challenges_names = [element.find('h4', {'class': 'challengecard-title'}).find(text=True, recursive=False) for element in challenge_list]

regex_diff = re.compile('difficulty')
regex_score = re.compile('max-score')
regex_success = re.compile('success-ratio')

for name, ch in tqdm(zip(challenges_dict.keys(), challenge_list), total=len(challenge_list)):
    title = ch.find('h4', {'class': 'challengecard-title'}).find(text=True, recursive=False)
    difficulty = ch.find('span', {'class': regex_diff}).get_text()
    score = ch.find('span', {'class': regex_score}).get_text()
    success = ch.find('span', {'class': regex_success}).get_text()
    link = 'https://www.hackerrank.com' + str(ch['href']) + '/problem'
    driver.get(link)
    description = driver.find_element_by_class_name('hackdown-content').text
    challenges_dict[name]['Title'] = title
    challenges_dict[name]['Description'] = description
    challenges_dict[name]['Link'] = link
    challenges_dict[name]['Difficulty'] = difficulty
    challenges_dict[name]['Score'] = score
    challenges_dict[name]['Success'] = success
    
    time.sleep(1.5)
    
with open("challenges.json", "w") as outfile: 
    json.dump(challenges_dict, outfile)