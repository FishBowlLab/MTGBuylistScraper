import progressbar, time, random, os
import pandas as pd
from Card import Card

class Scraper:
    def __init__(self,setName:str, setData:pd.DataFrame) -> None:
        self.setName=setName
        self.setData=setData
        self.exportFileName=setName +'_buylist.csv'
        self.buyList=[]
        self.bar=progressbar.ProgressBar(max_value=len(setData.index))
        
    # How do I specify that cards is a list of card objects in the parameters?
    def exportData(self, cards:list[Card])->pd.DataFrame: 
        header=['Name', 'Set', 'Condition', 'Finish', 'Price']
        df=pd.DataFrame(columns=header)
        for card in cards:
            df=pd.concat([df, card.exportToDf()], ignore_index=True)        # This looks like a really space inefficient way of appending
        return df
      
    def writeToFile(self):
        """Writes lines of the buylist cards into a csv file

        Args:
            fileName (str, optional): Name of the buylist file Defaults to 'setName_buylist.csv'.
        """
        lines=self.exportData(self.buyList)      #This doesn't exist right now
        exists=os.path.isfile(self.exportFileName)
        writingMode='a'
        if not exists:
            writingMode='w'
            exists=not exists
        lines.to_csv(self.exportFileName, mode=writingMode, header=exists, index=False)
        
    def delay(self):
        """Sleep function to prevent overloading the site. Range is between 1.5-4.5 seconds
        """
        delay=random.randint(1500, 4500)/1000
        print('delaying:', delay, 'seconds')    # Remove after debugging
        time.sleep(delay)