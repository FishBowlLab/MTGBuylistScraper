from CardData import CardData
from F2FScraper import F2FScraper
from Scraper401Games import Scraper401Games

class Builder:
    def __init__(self, fileName:str) -> None:
        """Builder object that interfaces with all the data objects and scraper objects

        Args:
            fileName (str): The MTGJSON containing all the card data and set information
        """
        self.fileName=fileName
        self.setData=CardData(fileName).cardNames()     
        self.validSources=['F2F', '401Games']       # List of sites that the scraper is capable of checking
        # Card list needs to be defined outside to be reused
        
    def removeDuplicates(self):
        '''
            This should search the DB for whether the card in setData has been scraped in a previous process.
            If it finds duplicates, it should remove it from self.setData before passing it onto the scraper
        '''
        pass
        
    def scrape(self, source:str, mode)->None:
        """Scrapes all cards from the setData from the specified source

        Args:
            source (str): Name of site's buylist to be scraped
            mode (str): Writes data into a file on the local drive. Modes include csv or db.
        """
        setName=self.fileName.split('.')[0]                 # removes the extension from the JSON for cleaner naming
        '''
        # This is an option to automate across all sites. 
        if source=='all':
            for site in self.validSources:
                pass
        '''
        # Add validation step here for valid sources as we build
        if source=="F2F":
            scrape=F2FScraper(setName, self.setData, mode)        #Scraper might be expecting a df instead of a series
        if source=='401Games':
            scrape=Scraper401Games(setName, self.setData, mode)
        scrape.scrapeAll()
    
    def scrapeAll(self, mode):
        for store in self.validSources:
            self.scrape(store, mode)
        
if __name__ == '__main__':
    build=Builder('KTK.json')
    #build.scrape('F2F', mode='db')
    build.scrape('401Games', mode='db')
    #build.scrapeAll(mode='db')    