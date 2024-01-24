import requests, bs4, time

def delay(t=100):
    time.sleep(t)
'''
# generate URL
def generate_url(cardName="Underground Sea", site='faceToFace'):
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

buyListOptions=[]
'''
Each card inside the cardlist is an <li> tag containing the card's information
Although I'm not a fan of how hard coded the find function is at the moment, it's the best prototype at the moment to successfully grab 
the values we want.
'''
cardList=page.select('.product')
for card in cardList:
    cardSet=card.find('p', {'class':'card-set'}).text
    cardPrice=float(card.find('span', {'class':'price--withoutTax'}).text.replace('$',''))  #think about setting to 2 decimal places
    
    # Testing BuyListObject <-- consider renaming since it's early
    
