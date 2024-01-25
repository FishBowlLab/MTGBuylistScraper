import requests, bs4, time, os, csv, random
from Card import Card

class F2FScraper:
    def __init__(self, setFile) -> None:
        # Feed a set into the file document
        self.setFile=setFile
        # Holds all cards found
        self.buyListOptions=[] 
        self.exportFileName=setFile+'_buylist.csv'
        # Using this dictionary hopefully makes things a bit easier to work with for other sites that use a different 
        # naming and tag system
        # Nested Dictionary. Is there a better way to map this like with a JSON?
        self.fields = {'set': {
                        'tag':'p',
                        'class':'card-set'
                        },
                        'price': {
                            'tag': 'span',
                            'class': 'price--withoutTax'
                        }
                    }
    
    def generate_url(self, cardName:str):
        cardName = cardName.lower().replace(' ','%20')
        return 'https://buylist.facetofacegames.com/search.php?search_query={}&section=product'.format(cardName)

    def delay(self):
        """Sleep function to prevent overloading the site
        """
        time.sleep(random.randint(500, 2500))

    # How do I specify that cards is a list of card objects in the parameters?
    def exportData(self, cards:list[Card]) -> list[list[str]]: 
        data=[]
        for card in cards:
            data.append(card.export())
        return data
    
    def writeToFile(self):
        """Writes lines of the buylist cards into a csv file

        Args:
            fileName (str, optional): Name of the buylist file Defaults to 'setName_buylist.csv'.
        """
        lines=self.exportData(self.buyListOptions)
        # Checks to see if file is created or not
        if not os.path.isfile(self.exportFileName):
            header=['Name', 'Set', 'Condition', 'Finish', 'Price']
            with open(self.exportFileName, 'w', newline='') as file:
                writer=csv.writer(file)
                writer.writerow(header)
        with open(self.exportFileName, 'a', newline='') as file:
            writer=csv.writer(file)
            writer.writerows(lines)
            
    def scrapeCard(self, cardName):
        # generate URL
        url=self.generate_url(cardName)
        res=requests.get(url)   # downloads the searched page   
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
            cardSet=card.find(self.fields['set']['tag'], {'class':self.fields['set']['class']}).text
            cardPrice=float(card.find(self.fields['price']['tag'], {'class':self.fields['price']['class']}).text.replace('$',''))  #think about setting to 2 decimal places
            self.buyListOptions.append(Card(cardName, cardSet, cardPrice))
    
    def scrapeFile(self):
        # loops the scrape card method for all cards inside the file.
        with open(self.setFile, 'r') as file:
            reader=csv.reader(file)
            next(reader)    # Skips the header fo the file
            for row in reader:
                self.scrapeCard(''.join(row))
                self.delay()
        self.writeToFile()

if __name__ == '__main__':
    scrape=F2FScraper('testFile.csv')
    scrape.scrapeFile()