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
print(df['name'])
#print(type(df.iloc[1])) #this is a series that looks to need to be converted back to a df