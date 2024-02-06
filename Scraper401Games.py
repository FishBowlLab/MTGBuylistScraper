from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from Card import Card
from Scraper import Scraper

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
    
    def initDriver(self):
        # Open up driver
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.delay()
        # Get access to the search screen for the buylist
        elem = self.driver.find_element(By.XPATH,  "//*[contains(@src, 'Magic-the-Gathering')]").find_element(By.XPATH, '..')
        elem.click()
        self.delay()

    def searchCard(self, cardName:str):
        # Fills in the search bar with the card name
        search=self.driver.find_element(By.CLASS_NAME, 'search-text')
        search.send_keys(cardName)
        self.delay()
        search.send_keys(Keys.RETURN)
        self.delay()
        
    def scrapeCard(self, cardName:str):
        pass
        #self.searchCard(cardName)
        # Select all cards 
    
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
    #scrape.scrapeAll()