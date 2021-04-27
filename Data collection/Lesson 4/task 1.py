from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
import time
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = MongoClient('localhost', 27017)
db = client['box']
massages = db.masseges

chrome_options = Options()
driver = webdriver.Chrome()

driver.get('https://e.mail.ru/')
elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-1-1-74')))
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)
time.sleep(1)
password = driver.find_element_by_name('password')
password.send_keys('o%IyneXIrI11')
password.send_keys(Keys.ENTER)

time.sleep(3)
m = driver.find_element_by_xpath('//a[@class="nav__item js-shortcut nav__item_active nav__item_shortcut nav__item_expanded_true nav__item_child-level_0"]')
total = m.get_attribute('title').split(' ')[1]
total = int(total)
links = []


while len(links) != total:
    time.sleep(1)
    income = driver.find_elements_by_xpath("//a[contains(@class,'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]")
    for pos in income:
        link = pos.get_attribute('href')
        if link not in links:
            links.append(link)
    actions = AC(driver)
    actions.move_to_element(income[-1])
    income[-1].send_keys(Keys.PAGE_DOWN)
    actions.perform()
    income = driver.find_elements_by_xpath('//a[@tabindex="-1"]')


for i in links:
    driver.get(i)
    time.sleep(1)
    massage = {}
    id = i.split('/')[-2]
    date = driver.find_element_by_class_name('letter__date').text
    text = driver.find_element_by_class_name('letter__body').text
    _from = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    massage['_id'] = id
    massage['date'] = date
    massage['text'] = text
    massage['from'] = _from
    massages.update_one({'_id': massage['_id']}, {'$set': massage}, upsert=True)


print(massages)
