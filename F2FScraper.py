import requests, bs4, time, os, csv, random, progressbar
import pandas as pd
import numpy as np
from Card import Card

class F2FScraper:
    def __init__(self, setFile:str) -> None:
        # Feed a set into the file document
        self.setFile=setFile
        # Holds all cards found
        self.buyListOptions=[] 
        self.exportFileName=setFile.replace('.csv','_buylist.csv')  #fix for when they add a .txt file later.
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
        self.bar=progressbar.ProgressBar(max_value=len(pd.read_csv(self.setFile)))
        
    def generate_url(self, cardName:str):
        cardName = cardName.lower().replace(' ','%20')
        return 'https://buylist.facetofacegames.com/search.php?search_query={}&section=product'.format(cardName)

    def delay(self):
        """Sleep function to prevent overloading the site. Range is between 1.5-4.5 seconds
        """
        delay=random.randint(1500, 4500)/1000
        print('delaying:', delay, 'seconds')    # Remove after debugging
        time.sleep(delay)


    # How do I specify that cards is a list of card objects in the parameters?
    def exportData(self, cards:list[Card], mode='csv'): 
        if mode=='csv':
            data=[]
            for card in cards:
                data.append(card.export())
            return data
        # Added this code in for when we can optimize the pandas approach
        if mode=='df':
            header=['Name', 'Set', 'Condition', 'Finish', 'Price']
            df=pd.DataFrame(columns=header)
            for card in cards:
                df=pd.concat([df, card.exportToDf()], ignore_index=True)        # This looks like a really space inefficient way of appending
            return df
        return []
    
    def writeToFile(self, mode='csv'):
        """Writes lines of the buylist cards into a csv file

        Args:
            fileName (str, optional): Name of the buylist file Defaults to 'setName_buylist.csv'.
        """
        if mode=='csv':
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
                
        # Done with pandas
        if mode=='df':
            exists=os.path.isfile(self.exportFileName)
            writingMode='a'
            if not exists:
                writingMode='w'
                exists=not exists
            lines.to_csv(self.exportFileName, mode=writingMode, header=exists, index=False)
            
    def scrapeCard(self, cardName):
        # generate URL
        url=self.generate_url(cardName)
        print(url)                      # Remove after debugging
        res=requests.get(url)           # downloads the searched page   
        # Returns an error if there's an issue with the response
        res.raise_for_status()
        print('Request Successful')     # Remove after debugging
        page=bs4.BeautifulSoup(res.text, 'html.parser')
        print('bs4 scraping')           # Remove after debugging
 
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
            self.buyListOptions.append(Card(cardName, cardSet, cardPrice))
        
    def scrapeFile(self):
        # loops the scrape card method for all cards inside the file.
        with open(self.setFile, 'r') as file:
            reader=csv.reader(file)
            next(reader)            # Skips the header fo the file
            print("File Opened")    # Remove after debugging
            try:
                for row in reader:
                    self.scrapeCard(''.join(row))
                    self.bar.update(1)
                    self.delay()
            except:
                print('An error has occured. Writing previously scraped data')
            finally:
                print('writing to file')        # Remove after debugging
                self.writeToFile()
                print("Done")

if __name__ == '__main__':
    scrape=F2FScraper('testFile.csv')
    scrape.scrapeFile()