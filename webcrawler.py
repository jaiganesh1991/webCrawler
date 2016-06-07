import sys
from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

#This is the Main entry point for the program
#This obtains the URL and search word from the user as text input during run time

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag=='a':
            for (key, value) in attrs:
                if key=='href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]


    def getLinks(self, url):
        print("inside getLinks")
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        headerDetails,decoder = response.getheader('Content-Type').split(';')
        print(headerDetails,decoder)
        print(headerDetails, "header details")
        headerFormat = 'text/html'
        print(headerDetails == headerFormat)
        if headerFormat == headerDetails:
            print("inside if condi")
            htmlBytes = response.read()
            htmlString = htmlBytes.decode(decoder)
            print(htmlString)
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]


def crawlerweb(url,searchWord):
    #print("starting program")
    pageToVisit = [url]
    visitCount = 0
    wordFoundStatus = False
    #print(not wordFoundStatus)
    maxPage = 150 #This is set to read a set of pages and return data
    #print(maxPage)
    while visitCount < maxPage and pageToVisit != [] and not wordFoundStatus:
        print("Entering while condition")
        visitCount = visitCount + 1
        url = pageToVisit[0]
        pageToVisit = pageToVisit[1:]
        print("visiting page is ", url)
        try:
            print(visitCount, "visiting URL", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                wordFoundStatus = True
                pagesToVisit = pagesToVisit + links
        except:
            print("Falied")
    if(wordFoundStatus == True):
        print("Found the Search word in URL", url)
    else:
        print("Word never found")
		
#Obtaining input from user
userInput = str(sys.argv)
#print(sys.argv)
#print(len(sys.argv))
#below condition checks if the URL and search string is passed
if len(sys.argv) != 3:
    print("Please input URL and search string. 2 Arguments only")
else:
    url = sys.argv[1]
    searchWord = sys.argv[2]
    crawlerweb(url,searchWord)
