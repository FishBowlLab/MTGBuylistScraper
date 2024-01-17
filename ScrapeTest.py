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

#cardList=page.select('.product')
#print(type(cardList))

# Brute Force
characteristics=['.card-name', '.card-set', '.card-condition', '.card-finish', '.price--withoutTax']

#nameList=page.select('.card-name')
#setList=page.select()