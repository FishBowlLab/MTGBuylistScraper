import pandas as pd

class Card:
    def __init__(self, name:str, set:str, source:str, price:str, condition:str="NM", finish:str="non-foil") -> None:
        """Card object that contains all fields from scraping

        Args:
            name (str): Card name
            set (str): The set the card was printed
            source (str): The site the data originated from
            price (str): Buylist price of item
            condition (str, optional): HP, SP, or NM Defaults to "NM".
            finish (str, optional): Version of the card. Defaults to "non-foil".
        """
        self.name=name
        self.set=set
        self.condition=condition           # NM/SP/HP
        self.finish=finish                 # foil/non-foil/special printing
        self.source=source
        self.price=price
    
    def display(self):
        """Prints out the attributes that are scraped.
        """
        print(
            '''
            Card Name: {name}
            Card Set: {set}
            Card Price: {price}
            '''.format(name=self.name, set=self.set, price=self.price)
        )
        
    def export(self)->list:
        """ Preps data to be exported to file

        Returns:
            list: List of strings containing all the attributes of the card
        """
        #return [self.name, self.set, self.condition, self.finish, str(round(self.price, 2))]
        return [self.name, self.set, self.condition, self.finish, self.source, self.price]
    
    def exportToDf(self)->pd.DataFrame:
        """Preps data to be exported to file using pandas
        Returns:
            pd.DataFrame: Single row of a Dataframe containing 
        """
        return pd.DataFrame([{
            'Name':self.name,
            'Set':self.set,
            'Condition':self.condition,
            'Finish':self.finish,
            'Source': self.source,
            'Price':self.price
        }])