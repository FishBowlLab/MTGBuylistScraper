import pandas as pd

# This attempts do format the column data into a php array in 1 step
def formatToStrPHPArray(value, key):
    return '"{key}"=>"{value}"'.format(key=key, value=value)

def formatToIntPHPArray(value, key):
    return '"{key}"=>{value}'.format(key=key, value=value)

def writePHPArray(df:pd.DataFrame):
    # First replace removes the leading '"
    # Second replace removes "'
    # Third replace fixes the formating on prices
    return str(df.values.tolist()).replace("\'\"", "\"").replace("\"\'", "\"").replace("']", "]")

cards='Dual Lands_buylist_401.csv'
df=pd.read_csv(cards)

for col in df.columns:
    if col=='Price':
        df[col]=df[col].apply(formatToIntPHPArray, args=(col,))
    else:        
        df[col]=df[col].apply(formatToStrPHPArray, args=(col,))
        
template='CardSeeder.php'
with open(template, 'r') as file:
    data=file.readlines()

# Search for line to replace
target='$cards =[];'
for i in range(len(data)):
    if target in data[i]:
        data[i]='\t\t$cards ={arr};\n'.format(arr=writePHPArray(df))

with open(template, 'w') as file:
    file.writelines(data)