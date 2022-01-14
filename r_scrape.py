import csv
import time

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Put chrome driver path here
browser = webdriver.Chrome("./chromedriver")

# Enter your route here
search_query_string = "restaurants in bangalore chennai highway"
more_places_css_selector = ".MXl0lf.tKtwEb.wHYlTd"
r_xpath = "//div[@jsname = 'GZq3Ke']"
r_name_xpath = "//*[@class='SPZz6b']//span"
r_address_xpath = "//*[@class='LrzXr']"
r_phone_css_selector = ".LrzXr.zdqRlf.kno-fv"
r_close_xpath = "//*[@class='QU77pf']"
next_page_id = "pnnext"


def add_key(by, value, obj, key):
    try:
        obj[key] = browser.find_element(by, value).text
    except NoSuchElementException:
        pass


def check_exists(by, value):
    try:
        browser.find_element(by, value)
    except NoSuchElementException:
        return False
    return True


def check_exists_text(by, value):
    while not check_exists(by, value):
        continue
    return len(browser.find_element(by, value).text) > 0


def check_exists_or_wait(by, value):
    while not check_exists_text(by, value):
        time.sleep(2)


def parse_restaurant():
    check_exists_or_wait(By.XPATH, r_name_xpath)
    restaurant = {
        "name": browser.find_element(By.XPATH, r_name_xpath).text,
        "address": browser.find_element(By.XPATH,
                                        r_address_xpath).text if check_exists(By.XPATH, r_address_xpath) else "",
        "phone": browser.find_element(By.CSS_SELECTOR,
                                      r_phone_css_selector).text if check_exists(By.CSS_SELECTOR,
                                                                                 r_phone_css_selector) else "",
    }
    print(restaurant)
    return restaurant


def res_page(rest_dict):
    div_length = len(browser.find_elements(By.XPATH, r_xpath))
    for i in range(div_length):
        browser.find_elements(By.XPATH, r_xpath)[i].click()
        rest_dict.append(parse_restaurant())
        browser.find_element(By.XPATH, r_close_xpath).click()
        time.sleep(2)


start_time = time.time()
restaurants = []
try:
    browser.get('http://www.google.com')
    search = browser.find_element(By.NAME, "q")
    search.send_keys(search_query_string)
    search.send_keys(Keys.RETURN)

    browser.find_element(By.CSS_SELECTOR, more_places_css_selector).click()

    while check_exists(By.ID, next_page_id):
        res_page(restaurants)
        browser.find_element(By.ID, next_page_id).click()
        time.sleep(2)

    print(len(restaurants))
    print(restaurants)

finally:
    browser.quit()
    if len(restaurants) > 0:
        keys = restaurants[0].keys()
        a_file = open("output.csv", "w")
        dict_writer = csv.DictWriter(a_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(restaurants)
        a_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
