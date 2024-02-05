import pandas as pd

'''
import json
fileName='Set Data/KTK.json'
with open(fileName, errors='ignore') as f:
    print(f)
    data=json.load(f)
    #print(data['data']['cards'])
'''
#df=pd.read_json('Set Data/KTK.json', orient='index', encoding='utf-8')
#print(type(df.iloc[1]['cards']))
#df=pd.read_json('Set Data/KTK.json', orient='index').iloc[1]['cards']

#Is there a better way to convert this after flipping it from DF->list->DF?
df=pd.DataFrame(pd.read_json('Set Data/KTK.json', orient='index').iloc[1]['cards'])
basic_lands=['Plains', 'Swamp', 'Forest', 'Mountain', 'Island']
'''
count=0
for item in df['name']:
    #Does this work if the name of the basic is in the name? Ex: Mountain Lion
    if item.lower() not in basic_lands:
        count+=1
print(count)
'''
'''
# There has to be a faster way of doing this rather than iterating across the df for each basic and redefining the df
for land in basic_lands:
    df=df.drop(df[df['name']==land].index)

'''
# https://saturncloud.io/blog/how-to-remove-rows-with-specific-values-in-pandas-dataframe/#:~:text=Another%20method%20to%20remove%20rows,value%20we%20want%20to%20remove.
df=df.drop(df[df['supertypes'][0]=='Basic'].index)

#for col in df.columns:
#    print(col)
#print(df['name'].tail(10))
print(df[['name', 'type']].tail(10))
#print(df['supertypes'])
#print(type(df['supertypes'][0]))

# Test code for searching up the df containing all the sets
'''
targetFalse='Alchemy 2023'
targetTrue='Tenth Edition'
df=pd.read_csv('Set Data\sets.csv')
setList=df[['name']].where(df['isOnlineOnly']==False).dropna()
#Checks if the target is in any row of any column
print(setList.isin([targetTrue]).any().any())
#print(df)
'''