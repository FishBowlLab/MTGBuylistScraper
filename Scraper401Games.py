from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from Card import Card
from Scraper import Scraper
import bs4

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
    
    def initDriver(self):
        # Open up driver
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.delay()
        # Get access to the search screen for the buylist
        elem = self.driver.find_element(By.XPATH,  "//*[contains(@src, 'Magic-the-Gathering')]").find_element(By.XPATH, '..')
        elem.click()
        self.delay()

    def cleanPrice(self, price:str)->str:
        return price.split('$')[1].replace(',','' )
    
    def searchCard(self, cardName:str)->bs4.BeautifulSoup:
        """Uses Selenium to find the card on a REact Site and returns a Beautiful Soup object ready for html parsing

        Args:
            cardName (str): Name of card we are looking up

        Returns:
            bs4.BeautifulSoup: Beautiful Soup object for html parsing
        """
        # Fills in the search bar with the card name
        search=self.driver.find_element(By.CLASS_NAME, 'search-text')
        search.send_keys(cardName)
        self.delay()
        search.send_keys(Keys.RETURN)
        '''
            TODO: Set Selenium up so that it will wait for load events before continuing with brute force
        '''
        self.delay()
        pageSource = self.driver.page_source   
        search.clear()
        self.delay() 
        return bs4.BeautifulSoup(pageSource, 'html.parser')
        
    def scrapeCard(self, cardName:str):
        page=self.searchCard(cardName)          # This feels a bit like Spaghetti code where I have a chain of things calling instead of a central method calling things
        cardList=page.select('.buylist-product') 
        for card in cardList:
            
            name=card.find(self.fields['name']['tag'], {'class':self.fields['name']['class']}).text
            # Skips cards that have partial matches from the initial search
            if cardName not in name:
                continue
            
            print(cardName)
            cardSet=card.find(self.fields['set']['tag'], {'class':self.fields['set']['class']}).find(self.fields['set']['child']).text
            print(cardSet)
            cardPrice=self.cleanPrice(card.find(self.fields['price']['tag']).text)
            print(cardPrice)
            self.buyList.append(Card(cardName, cardSet, '401Games', cardPrice))
    
    def scrapeAll(self):
        """Main method used to scrape the list of cards passed into the scraper
        """
        self.initDriver()
        try:
            for card in self.setData:
                print("Scraping", card)
                self.scrapeCard(card)
                self.delay()
        except:
            print('An error has occured. Writing previously scraped data')
        finally:
            self.driver.close()                # Should this be in its own method? Especially since the init is in its own method
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