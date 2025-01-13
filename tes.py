from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import multiprocessing
from fake_useragent import UserAgent
import undetected_chromedriver as uc

auth_page = "https://academic.ui.ac.id/main/Authentication/"
home_page = "https://academic.ui.ac.id/main/Welcome/Index"
siak_page = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
ua = UserAgent()
user_agent = ua.random

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--disable-gpu')
options.add_argument(f'user-agent={user_agent}')
driver = uc.Chrome(options=options)
driver_ua = driver.execute_script("return navigator.userAgent")
driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier":"1"})
print("User agent:")
print(driver_ua)
username = "ezar.akhdan"
password = "@1Dewi1@"
try:
    time.sleep(1)
    driver.get(auth_page)
    element = driver.find_element(By.ID, "u")
    time.sleep(1)
    element.send_keys(username)
    element = driver.find_element(By.NAME, "p")
    time.sleep(1)
    element.send_keys(password)
    time.sleep(1)
    element.send_keys(Keys.RETURN)

except Exception as e:
    if "Logout Counter" in driver.page_source :
        print("Logged in!")
        



try:
    time.sleep(1)
    driver.get(siak_page)
    if "Logout Counter" in driver.page_source :
        print("Logged in!")
except:
    print("lol")

input()