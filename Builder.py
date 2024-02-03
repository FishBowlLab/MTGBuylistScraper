from CardData import CardData
from F2FScraper import F2FScraper

class Builder:
    def __init__(self, fileName, source) -> None:
        self.fileName=fileName
        self.setData=CardData(fileName)
        self.source=source
        
    def scrape(self):
        # Add validation step here for valid sources as we build
        validSources=['F2F']
        
        if self.source=='F2F':
            scrape=F2FScraper(self.fileName)    #Edit code so it recieves the DF instead
            scrape.scrapeFile()
        
if __name__ == '__main__':
    build=Builder('KTK.json')
    