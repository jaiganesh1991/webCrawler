import sys
from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

#This is the Main entry point for the program
#This obtains the URL from the user as text input during run time

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag=='a' or tag=='link':
            for (key, value) in attrs:
                if key=='href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        headerDetails,decoder = response.getheader('Content-Type').split(';')
        headerFormat = 'text/html' #setting header to read only html files
        charterset,realDecoder = decoder.split('=')
        #condition check if the reading page is Text based html file
        if headerFormat == headerDetails:
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8") #Defaulted to Decoding with the utf-8 
            self.feed(htmlString)
            self.handle_starttag('a',[('href',self.baseUrl)])
            self.handle_starttag('link',[('href',self.baseUrl)])
            return htmlString, self.links
        else:
            return "",[]


def crawlerweb(url):
    pageToVisit = [url]
    visitCount = 0
    maxPage = 500 #This is set to read a set of pages and return data
    #Condition to iterate over the given URL and find the HREF
    while visitCount < maxPage and pageToVisit != []:
        visitCount = visitCount + 1
        url = pageToVisit[0]
        pageToVisit = pageToVisit[1:]
        visitedPages = []
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
            visitedPages = visitedPages + links
        except:
            print("Exception is handled")
        print("site map is ")
        while (len(visitedPages) - 1) != 0:
            print(visitedPages[0])
            visitedPages = visitedPages[1:]
#Obtaining input from user
userInput = str(sys.argv)
#below condition checks if the URL is passed
if len(sys.argv) != 2:
    print("Please input URL and search string. 1 Arguments only")
else:
    url = sys.argv[1] #Assigns URL
    crawlerweb(url) #Calls the function crawlerweb by passing the URL and Search word
