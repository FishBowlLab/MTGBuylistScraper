import requests, bs4, time, os, csv
from Card import Card

testCard="Underground Sea"

def delay(t=100):
    time.sleep(t)
    
def writeToFile(lines:list[list[str]], fileName='setName.csv'):
    # Checks to see if file is created or not
    if not os.path.isfile(fileName):
        header=['Name', 'Set', 'Condition', 'Finish', 'Price']
        with open(fileName, 'w') as file:
            writer=csv.writer(file)
            writer.writerow(header)
    with open(fileName, 'a') as file:
        writer=csv.writer(file)
        writer.writerows(lines)

# How do I specify that cards is a list of card objects in the parameters?
def exportData(cards:list[Card]) -> list[list[str]]: 
    data=[]
    for card in cards:
        print(card)
        data.append(card.export())
    return data
'''
# generate URL
def generate_url(cardName=testCard, site='faceToFace'):
    # Use 
    if site=="faceToFace":
        cardName = cardName.lower().replace(' ','%20')
        return 'https://buylist.facetofacegames.com/search.php?search_query={}&section=product'.format(cardName)
    # return empty URL if there's an error
    return ''

url=generate_url()
res=requests.get(url)   # downloads the searched page

# Returns an error if there's an issue with the response
res.raise_for_status()

page=bs4.BeautifulSoup(res.text, 'html.parser')
'''
testFile = open('Face To Face Games Buylist.html')      
page=bs4.BeautifulSoup(testFile.read(), 'html.parser')

# Using this dictionary hopefully makes things a bit easier to work with for other sites that use a different 
# naming and tag system
F2F_fields={
    # Nested Dictionary. Is there a better way to map this like with a JSON?
    'set': {
        'tag':'p',
        'class':'card-set'
    },
    'price': {
        'tag': 'span',
        'class': 'price--withoutTax'
    }
}

# Holds all cards found
buyListOptions=[]
'''
Each card inside the cardlist is an <li> tag containing the card's information
Although I'm not a fan of how hard coded the find function is at the moment, it's the best prototype at the moment to successfully grab 
the values we want.
'''
cardList=page.select('.product')
for card in cardList:
    cardSet=card.find(F2F_fields['set']['tag'], {'class':F2F_fields['set']['class']}).text
    cardPrice=float(card.find(F2F_fields['price']['tag'], {'class':F2F_fields['price']['class']}).text.replace('$',''))  #think about setting to 2 decimal places
    buyListOptions.append(Card(testCard, cardSet, cardPrice))

writeToFile(exportData(buyListOptions))