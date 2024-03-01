import requests, bs4, progressbar, re
import pandas as pd
from Card import Card
from Scraper import Scraper

class F2FScraper(Scraper):
    def __init__(self, setName:str, setData:pd.Series) -> None:
        """Scraper dedicated to parsing through FaceToFaceGames using a query string

        Args:
            setName (str): Name of the MTG set for scraping
            setData (pd.Series): Series containing the cleaned set of card names from the MTGJSON
        """
        Scraper.__init__(self, setName, setData)
        self.bar=progressbar.ProgressBar(max_value=len(setData.index))
        # Using this dictionary hopefully makes things a bit easier to work with for other sites that use a different 
        # naming and tag system
        # Nested Dictionary. Is there a better way to map this like with a JSON?
        self.fields = {'name':{
                            'tag':'p',
                            'class':'card-name'
                        },
                        'set':{
                            'tag':'p',
                            'class':'card-set'
                        },
                        'price':{
                            'tag': 'span',
                            'class': 'price price--withoutTax'
                        }
                    }
        
    def generate_url(self, cardName:str)->str:
        """Generates the query string for FaceToFaceGames

        Args:
            cardName (str): Name of the card to search for

        Returns:
            _type_: The URL for the query string for FaceToFaceGames
        """
        cardName = cardName.lower().replace(' ','%20')
        return 'https://buylist.facetofacegames.com/search.php?search_query={}&section=product'.format(cardName)

    def cleanPrice(self, price:str)->str:
        """Formats price element for FaceToFaceGames

        Args:
            price (str): Element containing the price of a card

        Returns:
            str: a string of the price removing all price related symbols and blank spaces
        """
        # Someone please tell me what this regex means
        return re.sub(r"(?:(?!\.)[\W])+", '', price)
    
    def scrapeCard(self, cardName:str):
        """Scrapes an individual card from FaceToFaceGames

        Args:
            cardName (str): The card name you are scraping
        """
    
        url=self.generate_url(cardName) # generate URL
        res=requests.get(url)           # downloads the searched page   
        res.raise_for_status()          # Returns an error if there's an issue with the response
        page=bs4.BeautifulSoup(res.text, 'html.parser')
 
        '''
        Each card inside the cardlist is an <li> tag containing the card's information
        Although I'm not a fan of how hard coded the find function is at the moment, it's the best prototype at the moment to successfully grab 
        the values we want.
        '''
        cardList=page.select('.product')
        for card in cardList:
            cardName=card.find(self.fields['name']['tag'], {'class':self.fields['name']['class']}).text.strip()     #re-using the card name variable
            cardSet=card.find(self.fields['set']['tag'], {'class':self.fields['set']['class']}).text
            
            # Skips appending card if the set is not valid
            if not self.isValidSet(cardSet):
                continue
            
            cardPrice=self.cleanPrice(card.find(self.fields['price']['tag'], {'class':self.fields['price']['class']}).text.split('-')[1])
            self.buyList.append(Card(cardName, cardSet,'FaceToFaceGames', cardPrice))
        
    def scrapeAll(self):
        """Main method used to scrape the list of cards passed into the scraper
        """
        try:
            for card in self.setData:
                print("Scraping", card)
                self.bar.update(1)
                self.scrapeCard(card)
                self.delay()
        except:
            print('An error has occured. Writing previously scraped data')
        finally:
            print('writing to file...')        # Remove after debugging
            self.writeToFile()
            print("Scraping Done")

if __name__ == '__main__':
    # For Testing
    data={
        "name":["Underground Sea", "Taiga"],
    }
    df=pd.DataFrame(data)['name']
    scrape=F2FScraper('Dual Lands', df)
    scrape.scrapeAll()