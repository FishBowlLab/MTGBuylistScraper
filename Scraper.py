import time, random, os
import pandas as pd

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
        
        self.exportFileName=setName +'_buylist.csv'                                 # Name of file to be written
        self.uploadTemplate='CardSeeder.php'
        self.targetStr='$cards =[];'
        self.buyList=[]                                                             # Holds all Card objects scraped
        
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
        #TODO: Adjust for partial matches since we can also account for foreign language cards like FBB
        return self.existingSets.isin([setName]).any().any()
    
    def addToBuyList(self, name:str, set:str, source:str, price:str, condition:str="NM", finish:str="non-foil")->None:
        self.buyList.append([name, set, condition, finish, source, price])
    
    # How do I specify that cards is a list of card objects in the parameters?
    def exportToDf(self)->pd.DataFrame: 
        """Preps list of cards into a dataframe to be processed

        Args:
            cards (list[Card]): List of card objects from the scraper 

        Returns:
            pd.DataFrame: Dataframe containing all buylist information
        """
        header=['Name', 'Set', 'Condition', 'Finish', 'Source', 'Price']
        return pd.DataFrame(self.buyList, columns=header).drop_duplicates()
    
    def setDBFile(self, file:str, targetStr:str)->None:
        self.uploadTemplate=file
        self.targetStr=targetStr
    
    def formatToStrPHPArray(self, value:str, key:str)->str:
        return '"{key}"=>"{value}"'.format(key=key, value=value)

    def formatToIntPHPArray(self, value:str, key:int)->str:
        return '"{key}"=>{value}'.format(key=key, value=value)
    
    def convertToPHPArray(self, df:pd.DataFrame)->str:
        for col in df.columns:
            if col=='Price':
                df[col]=df[col].apply(self.formatToIntPHPArray, args=(col,))
            else:        
                df[col]=df[col].apply(self.formatToStrPHPArray, args=(col,))
        return str(df.values.tolist())
        
    def writeToFile(self, mode='csv')->None:
        """Writes lines of the buylist cards into a file

        Args:
            mode (str, optional): Writes data into a file on the local drive. Modes include csv or db. Defaults to 'csv'.
        """
        '''
            Debating between upsert and batch
            Refer to the video: https://www.youtube.com/watch?v=2QhPLcYLay8&ab_channel=LaravelDaily
        '''
        lines=self.exportToDf()
        if mode=='csv':
            if os.path.isfile(self.exportFileName):
                writingMode='a'
                includeHead=False
            else:
                writingMode='w'
                includeHead=True
            lines.to_csv(self.exportFileName, mode=writingMode, header=includeHead, index=False)
            
        if mode=='db':
            with open(self.uploadTemplate, 'r') as file:
                data=file.readlines()

            for i in range(len(data)):
                 # Search for line to replace
                if self.targetStr in data[i]:
                    data[i]='\t\t$cards={arr};\n'.format(arr=self.convertToPHPArray(lines))

            with open(self.uploadTemplate, 'w') as file:
                file.writelines(data)
        
    def delay(self):
        """Sleep function to prevent overloading the site with requests. Delay range is between 1.5-4.5 seconds
        """
        delay=random.randint(1500, 4500)/1000
        print('delaying:', delay, 'seconds')    # Remove after debugging
        time.sleep(delay)
    