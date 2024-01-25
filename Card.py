class Card:
    def __init__(self, name, set, price) -> None:
        self.name=name
        self.set=set
        self.condition='NM'           # Fix this until I can parse the article tag     
        self.finish='non-foil'        # foil or regular
        self.price=price
    
    def display(self):
        print(
            '''
            Card Name: {name}
            Card Set: {set}
            Card Price: {price}
            '''.format(name=self.name, set=self.set, price=self.price)
        )
    def export(self):
        """ Preps data to be exported to file

        Returns:
            List of strings containing all the attributes of the card
        """
        return [self.name, self.set, self.condition, self.finish, str(round(self.price, 2))]