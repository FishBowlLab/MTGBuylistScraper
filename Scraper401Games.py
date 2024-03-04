from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scraper import Scraper
import pandas as pd
import bs4, math
#import progressbar

class Scraper401Games(Scraper):
    def __init__(self, setName: str, setData: pd.Series) -> None:
        """Scraper targeted for sites built with React that require Selenium to scrape since items are fetched using JS

        Args:
            setName (str): Name of the MTG set for scraping
            setData (pd.Series): Series containing the cleaned set of card names from the MTGJSON
        """
        super().__init__(setName, setData)
        self.url='https://buylist.401games.ca/retailer/buylist'
        self.driver = None
        self.fields={
            'name':{
                'tag':'div',
                'class':'product-title'
            },
            'set': {
                'tag':'div',
                'class':'product-set',
                'child': 'span',            # We need the span inside this for the set info
            },
            'price':{
                'tag': 'strong'
            }
        }
        # Limits selenium to scrape 40 times per iteration
        self.scrapeLimit=40
        #self.bar=progressbar.ProgressBar(max_value=len(setData.index))
    
    def initDriver(self):
        # Open up driver
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.delay()
        # Get access to the search screen for the buylist
        elem=WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@src, 'Magic-the-Gathering')]"))
        )
        elem=self.driver.find_element(By.XPATH, "//*[contains(@src, 'Magic-the-Gathering')]").find_element(By.XPATH, '..')
        elem.click()
        self.delay()

    def closeDriver(self):
        DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'
        if self.driver.get_log('driver')[-1]['message'] == DISCONNECTED_MSG:
            print("Driver has been closed")
        else:
            self.driver.close()

    def setScrapeLimit(self, limit)->None:
        self.scrapeLimit=limit

    def cleanName(self, name:str)->str:
        # This is very very hard coded. Consider a more elegant solution later
        return name.split('(')[0].strip()
    
    def cleanPrice(self, price:str)->str:
        return price.split('$')[1].replace(',','' )
    
    def searchCard(self, cardName:str)->bs4.BeautifulSoup:
        """Uses Selenium to find the card on a REact Site and returns a Beautiful Soup object ready for html parsing

        Args:
            cardName (str): Name of card we are looking up

        Returns:
            bs4.BeautifulSoup: Beautiful Soup object for html parsing
        """
        try:
            # Fills in the search bar with the card name
            search=WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-text"))
            )
            search.clear()
            search.send_keys(cardName)
            self.delay()
            search.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "buylist-product"))
            )
        except:
            # Probably create a log file for this
            print("An error has occured while scraping", cardName)
        finally:
            #self.delay()       # Unclear whether this delay is necessary
            pageSource = self.driver.page_source   
            search.clear()
            return bs4.BeautifulSoup(pageSource, 'html.parser')
        
    def scrapeCard(self, cardName:str):
        page=self.searchCard(cardName)          # This feels a bit like Spaghetti code where I have a chain of things calling instead of a central method calling things

        cardList=page.select('.buylist-product') 
        for card in cardList:
            
            name=card.find(self.fields['name']['tag'], {'class':self.fields['name']['class']}).text
            cardSet=card.find(self.fields['set']['tag'], {'class':self.fields['set']['class']}).find(self.fields['set']['child']).text
            cardFinish='non-foil'
            # Skips cards that have partial matches from the initial search
            if cardName not in name or not self.isValidSet(cardSet):
                continue
            if '(Foil)' in name:
                cardFinish='foil'
                    
            cardPrice=self.cleanPrice(card.find(self.fields['price']['tag']).text)
            self.addToBuyList(self.cleanName(name), cardSet, '401Games', cardPrice, finish=cardFinish)
    
    def scrapeAll(self):
        """Main method used to scrape the list of cards passed into the scraper
        """
        itter=math.ceil(len(self.setData.index)/self.scrapeLimit)
        #self.initDriver()
        try:
            # scrape in partitions based on the scrapeLimit
            for i in range(itter):
                self.initDriver()
                # This is a sloppy way of calculating the partitions we want to run the scraper
                startPt=self.scrapeLimit*i
                endPt=startPt+self.scrapeLimit
                # This accounts for the last iteration where we go out of bounds of the dataframe
                if endPt>len(self.setData.index):
                    endPt=len(self.setData.index)
                    
                for card in self.setData.iloc[startPt:endPt]:
                    print("Scraping", card)
                    #self.bar.update(1)
                    self.scrapeCard(card)
                self.driver.close()
                #self.closeDriver()
        except:
            print('An error has occured on {card}. Writing previously scraped data'.format(card))
        finally:
            #self.closeDriver()                # Should this be in its own method? Especially since the init is in its own method
            try:
                self.driver.close()
            except:
                print('Driver has already been closed')
                
            print('writing to file...')        # Remove after debugging
            self.writeToFile()
            print("Scraping Done")


if __name__ == '__main__':
    # For Testing
    data={
        "name":["Underground Sea", "Taiga"],
    }
    df=pd.DataFrame(data)['name']
    scrape=Scraper401Games('Dual Lands', df)
    scrape.scrapeAll()