from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, bs4

def delay():
    # This is temporary. Use Selenium's pre-built wait function
    time.sleep(1)

targetCard="Underground Sea"

def fetchPage():
    url='https://buylist.401games.ca/retailer/buylist'

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
    search.send_keys(targetCard)
    delay()
    search.send_keys(Keys.RETURN)
    delay()
    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(pageSource)
    fileToWrite.close()
    
    driver.close()

fields={
    # Nested Dictionary. Is there a better way to map this like with a JSON?
    'name':{
        'tag':'div',
        'class':'product-title'
    },
    # We need the span inside this for the set info
    'set': {
        'tag':'div',
        'class':'product-set',
        'child': 'span',
    },
    'price':{
        'tag': 'strong'
    }
}

# Code to grab page source for bs4 to read since bs4 is apparently a better html parser
#pageSource = driver.page_source    
#page=bs4.BeautifulSoup(pageSource, 'html.parser')

pageSource = open('page_source.html')      
page=bs4.BeautifulSoup(pageSource.read(), 'html.parser')
cardList=page.select('.buylist-product')

for card in cardList:
    cardName=card.find(fields['name']['tag'], {'class':fields['name']['class']}).text
    # Skips cards that have partial matches from the initial search
    if targetCard not in cardName:
        continue
    print(cardName)
    cardSet=card.find(fields['set']['tag'], {'class':fields['set']['class']}).find(fields['set']['child']).text
    print(cardSet)
    cardPrice=card.find(fields['price']['tag']).text.split('$')[1].replace(',','' )
    print(cardPrice)
    




# Grabbing done with Selenium. Probably less powerful than bs4
#items=driver.find_elements(By.CLASS_NAME, 'buylist-product')
#for item in items:
#    print(item)
