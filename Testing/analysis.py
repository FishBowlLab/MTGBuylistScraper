import pandas as pd

buyData=pd.read_csv('BuyList.csv')
data1=pd.read_csv('Dual Lands_buylist_f2f.csv')
data2=pd.read_csv('Dual Lands_buylist_401.csv')

target='Underground Sea'
setName="Unlimited Edition"

def searchDF(data, target, setName):
    return data[(data['Name']==target) & (data['Set']==setName)]

data1=buyData.merge(data1, on=['Name', "Set"], how='left')
data2=buyData.merge(data2, on=['Name', "Set"], how='left')


# Finds sum of each buylist
# Need to flag cards that were excluded from the buylist in the sums
print('F2F Buylist: $', data1['Price'].sum())
print('401 Buylist: $', data2['Price'].sum())
print('Cards excluded:')
for card in data2[data2.isna().any(axis=1)]['Name']:
    print(card)

# Merges
allData=pd.concat([data1, data2], ignore_index=True)
#print(allData)
idx=allData.groupby('Name')['Price'].idxmax()
bestPrices=allData.loc[idx]
print(bestPrices)
'''
   
    First thing I need to do is create a list to sell and return the df from each data containing the cards with matching name and set
        --> Calculate the sum of the cards from each small df and save into results
        
    Then join these df veritcally.
    Group by, sort, then drop all repeats besides the first.
    
    Sort the 
    
'''

#hdf=pd.concat([df, card.exportToDf()], ignore_index=True) 
#df.loc[df['column_name'].isin(some_values)]
#df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]
#print(data1.loc[data1['Name'].isin(["Underground Sea"])])
#print(data1[data1['Name']==target])
#print()
#print(data2)