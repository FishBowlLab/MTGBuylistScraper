from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def delay():
    # This is temporary. Use Selenium's pre-built wait function
    time.sleep(1)

url='https://buylist.401games.ca/retailer/buylist'
card="Underground Sea"

#opens page
driver = webdriver.Chrome()
driver.get(url)
delay()
#navigates to the buylist
elem = driver.find_element(By.XPATH,  "//*[contains(@src, 'Magic-the-Gathering')]").find_element(By.XPATH, '..')
delay()
elem.click()
delay()
#searches for card
search=driver.find_element(By.CLASS_NAME, 'search-text')
search.send_keys(card)
delay()
search.send_keys(Keys.RETURN)
delay()

# Code to grab page source for bs4 to read since bs4 is apparently a better html parser
pageSource = driver.page_source
fileToWrite = open("page_source.html", "w")
fileToWrite.write(pageSource)
fileToWrite.close()
fileToRead = open("page_source.html", "r")
print(fileToRead.read())
fileToRead.close()



# Grabbing done with Selenium. Probably less powerful than bs4
#items=driver.find_elements(By.CLASS_NAME, 'buylist-product')
#for item in items:
#    print(item)

driver.close()