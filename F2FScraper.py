import requests, bs4
import pandas as pd
from Card import Card
from Scraper import Scraper

class F2FScraper(Scraper):
    def __init__(self, setName:str, setData:pd.DataFrame) -> None:
        Scraper.__init__(self, setName, setData)
        
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
        
    def generate_url(self, cardName:str):
        cardName = cardName.lower().replace(' ','%20')
        return 'https://buylist.facetofacegames.com/search.php?search_query={}&section=product'.format(cardName)

    def scrapeCard(self, cardName):
        # generate URL
        url=self.generate_url(cardName)
        res=requests.get(url)           # downloads the searched page   
        # Returns an error if there's an issue with the response
        res.raise_for_status()
        page=bs4.BeautifulSoup(res.text, 'html.parser')
 
        '''
        Each card inside the cardlist is an <li> tag containing the card's information
        Although I'm not a fan of how hard coded the find function is at the moment, it's the best prototype at the moment to successfully grab 
        the values we want.
        '''
        cardList=page.select('.product')
        for card in cardList:
            cardName=card.find(self.fields['name']['tag'], {'class':self.fields['name']['class']}).text     #re-using the card name variable
            cardSet=card.find(self.fields['set']['tag'], {'class':self.fields['set']['class']}).text
            
            # TODO: Fix price scraping
            # This line needs to be adjusted so it's not scraping a range.
            # We skipped the float conversion because it was grabbing a range
            cardPrice=card.find(self.fields['price']['tag'], {'class':self.fields['price']['class']}).text.replace('$','')  
            self.buyList.append(Card(cardName, cardSet, cardPrice))
        
    def scrapeAll(self):
        # loops the scrape card method for all cards inside the dataframe.
        try:
            for card in self.setData['name']:
                print("Scraping", card)
                self.scrapeCard(card)
                self.bar.update(1)
                self.delay()
        except:
            print('An error has occured. Writing previously scraped data')
        finally:
            print('writing to file...')        # Remove after debugging
            self.writeToFile()
            print("Scraping Done")

if __name__ == '__main__':
    data={
        "name":["Underground Sea", "Taiga"],
    }
    df=pd.DataFrame(data)
    scrape=F2FScraper('Dual Lands', df)
    scrape.scrapeAll()