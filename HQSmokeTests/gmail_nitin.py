from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from datetime import date
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
driver.get("https://login.yahoo.com/")
driver.find_element_by_id("login-username").send_keys('nsaxenadimagi@yahoo.com')
driver.find_element_by_id("login-signin").click()
time.sleep(5)
driver.find_element_by_name("password").send_keys('jakeisbest')
driver.find_element_by_id("login-signin").click()
driver.find_element_by_xpath("//div[@class= 'icon mail']").click()
driver.find_element_by_xpath('//*[contains(text(),"Invitation from Nitin Saxena to join CommCareHQ")][1]').click()
####
p = driver.find_element_by_xpath('//div[@data-test-id="message-date"]')
date_extracted_by_selenium = p.text
print(date_extracted_by_selenium)
stripped_strings = re.findall(r'\w+', date_extracted_by_selenium)
unwanted = [0, 2]
for ele in unwanted:
    del stripped_strings[ele]
stripped_strings.insert(2, str(date.today().year))
###
datetime_object = datetime.strptime(" ".join(stripped_strings), '%d %b %Y %I %M %p')
print(datetime_object)
current_time = datetime.now()
print(current_time)
time_difference = print(round((current_time - datetime_object).total_seconds()))
assert time_difference not in range(0,180), "Mail not Received"
driver.close()
