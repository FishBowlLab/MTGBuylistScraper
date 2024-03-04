import pandas as pd

class BuyListAnalysis:
    def __init__(self, buylist:str) -> None:
        self.buylist=pd.read_csv(buylist)
        self.stores=['F2F', '401Games']

        # Placeholders until I decide how to fetch data
        self.dataF2F=pd.read_csv('Dual Lands_buylist_f2f.csv')
        self.data401=pd.read_csv('Dual Lands_buylist_401.csv')
        
    # This is an artifact of test code. Remove if not needed
    def searchDF(self, data, target, setName):
        return data[(data['Name']==target) & (data['Set']==setName)]
    
    # TODO: Figure out this method is going to access the DB 
    def fetchStore(self, source:str)->pd.DataFrame:
        # This is probably where it selects which data to grab from
        return self.buylist.merge(source, on=['Name', 'Set'], how='left')
    
    def fetchAllBuylists(self, sources:list[str]):
        buylists=[]
        for store in sources:
            buylists.append(self.fetchStore(store))
        return buylists
    
    def optimizePrice(self, data:list[pd.DataFrame])->pd.DataFrame:
        # Merges
        allData=pd.concat(data, ignore_index=True)
        idx=allData.groupby('Name')['Price'].idxmax()
        bestPrices=allData.loc[idx]
        return bestPrices
    
    def analysis(self):
        pass
    
    def report(self, source:str, data:pd.DataFrame)->None:
        for card in data[data.isna().any(axis=1)]['Name']:
            print(card, 'was not included')
        print('---------------------------------------')
        print(source,'Buylist Value: $', data['Price'].sum())
        
if __name__ == '__main__':
    # For Testing
    buylistFile='Buylist.csv'
    stores=['F2F', '401Games']
    myBuyList=BuyListAnalysis(buylistFile)
    buylistData=myBuyList.fetchAllBuylists(stores)  
    