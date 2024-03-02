import pandas as pd

class CardData:
    def __init__(self, fileName:str) -> None:
        """Creates an object that looks for JSON from MTGJSON and preps it for scraping

        Args:
            fileName (json): A JSON file located in the data folder
        """
        self.fileName=fileName
    
    def cardNames(self)->pd.Series:
        """Generates a Series containing only the card names in the set

        Returns:
            pd.Series: A series containing only the names of the cards passed by the MTGJSON
        """
        rawData=pd.DataFrame(pd.read_json('Set Data/{}'.format(self.fileName), orient='index').iloc[1]['cards'])
        rawData=self.removeDuplicates(self.removeBasics(rawData))
        # Add additional cleaning methods here as necessary
        
        return rawData['name']
    
    def removeBasics(self, rawData:pd.DataFrame)->pd.DataFrame:
        """Removes basic lands from the dataframe containing the card names

        Args:
            rawData (pd.DataFrame): Dataframe containing the data loaded from the MTGJSON

        Returns:
            pd.DataFrame: Dataframe without the basic lands in the list
        """
        basic_lands=['Plains', 'Swamp', 'Forest', 'Mountain', 'Island']
        # Slices the dataframe and drops all elements with names that are within the basic lands list
        return rawData[~rawData['name'].isin(basic_lands)]      
    
    def removeDuplicates(self, rawData:pd.DataFrame)->pd.DataFrame:
        return rawData.drop_duplicates(subset='name')
    
if __name__=='__main__':
    data=CardData('KTK.json')
    print(data.cardNames())