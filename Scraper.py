import time, random, os
import pandas as pd
from Card import Card

class Scraper:
    def __init__(self,setName:str, setData:pd.Series) -> None:
        """Parent object of scrapers. Handles all file reading and writing

        Args:
            setName (str): Name of the set intending to be scraped
            setData (pd.Series): A series containing the names of the cards for scraping
        """
        self.setName=setName
        self.setData=setData
        self.existingSets=self.populateExistingSets()
        
        self.exportFileName=setName +'_buylist.csv'             # Name of file to be written
        self.buyList=[]                                         # Holds all Card objects scraped
        
    def populateExistingSets(self)->pd.DataFrame:
        """Creates a dataframe containing all possible MTG sets in paper

        Returns:
            pd.DataFrame: Dataframe containing the names of all MTG sets
        """
        df=pd.read_csv('Set Data\sets.csv')
        return df[['name']].where(df['isOnlineOnly']==False).dropna()
    
    def isValidSet(self, setName:str)->bool:
        """Checks whether the card is in a valid mtg set 

        Args:
            setName (str): Name of set intended for scraping

        Returns:
            bool: True if set name is a valid MTG set
        """
        return self.existingSets.isin([setName]).any().any()
    
    # How do I specify that cards is a list of card objects in the parameters?
    def exportData(self, cards:list[Card])->pd.DataFrame: 
        """Preps list of cards into a dataframe to be processed

        Args:
            cards (list[Card]): List of card objects from the scraper 

        Returns:
            pd.DataFrame: Dataframe containing all buylist information
        """
        header=['Name', 'Set', 'Condition', 'Finish', 'Source', 'Price']
        df=pd.DataFrame(columns=header)
        for card in cards:
            df=pd.concat([df, card.exportToDf()], ignore_index=True)        # This looks like a really space inefficient way of appending
        return df
      
    def writeToFile(self):
        """Writes lines of the buylist cards into a csv file
        """
        lines=self.exportData(self.buyList)      #This doesn't exist right now
        exists=os.path.isfile(self.exportFileName)
        writingMode='a'
        if not exists:
            writingMode='w'
            exists=not exists
        lines.to_csv(self.exportFileName, mode=writingMode, header=exists, index=False)
        
    def delay(self):
        """Sleep function to prevent overloading the site with requests. Delay range is between 1.5-4.5 seconds
        """
        delay=random.randint(1500, 4500)/1000
        print('delaying:', delay, 'seconds')    # Remove after debugging
        time.sleep(delay)
    