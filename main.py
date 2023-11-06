import time, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_settings = webdriver.ChromeOptions()
chrome_settings.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_settings)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie_btn = driver.find_element(By.CSS_SELECTOR, "div #cookie")
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5

game_is_on = True
while game_is_on:
    cookie_btn.click()

    if time.time() > timeout:
        cookie_count = driver.find_element(By.CSS_SELECTOR, "div #money")
        upgrades = driver.find_elements(By.CSS_SELECTOR, "div #store > div > b")
        prices = []
        for upgrade in upgrades:
            text = upgrade.text
            if text != "":
                cost = int(upgrade.text.split("-")[1].strip().replace(',',''))
                prices.append(cost)

        upgrades = {}
        for n in range(len(prices)):
            upgrades[prices[n]] = item_ids[n]

        cookie_count = driver.find_element(by=By.ID, value="money").text
        if "," in cookie_count:
            cookie_count = cookie_count.replace(",", "")
        cookie_count = int(cookie_count)

        affordable_upgrades = {}
        for cost, id in upgrades.items():
            if cookie_count >= cost:
                affordable_upgrades[cost] = id

        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(by=By.ID, value=to_purchase_id).click()

        timeout = time.time() + 5


if time.time() > five_min:
    cookie_per_s = driver.find_element(by=By.ID, value="cps").text
    print(cookie_per_s)
    game_is_on = False

driver.quit()
