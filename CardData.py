import pandas as pd

class CardData:
    def __init__(self, fileName) -> None:
        self.fileName=fileName
        self.setList=self.cardNames()
    
    def cardNames(self):
        rawData=pd.DataFrame(pd.read_json('Set Data/{}'.format(self.fileName), orient='index').iloc[1]['cards'])
        rawData=self.removeBasics(rawData)
        # Add additional cleaning methods here as necessary
        
        return rawData['name']
    
    def removeBasics(self, rawData):
        basic_lands=['Plains', 'Swamp', 'Forest', 'Mountain', 'Island']
        # There has to be a faster way of doing this rather than iterating across the df for each basic and redefining the df
        for land in basic_lands:
            rawData=rawData.drop(rawData[rawData['name']==land].index)  
        return rawData      
    
if __name__=='__main__':
    data=CardData('KTK.json')
    print(data.setList)