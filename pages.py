import http.client #Used to make HTTP requests for a webpage
from html.parser import HTMLParser #Used to 'parse' the HTML to look for links
import urllib.parse #Used to parse URL components


class LinkParser(HTMLParser): #Class with a method overwrite to extrace links from <a> tags
    def __init__(self): #Setting up variables [NOT GREAT]
        super().__init__()
        self.urls = [] #Store all found links on the page as strings including realtive URLs
    def handle_starttag(self, tag, attrs): #Called when an HTML tag is encountered while parsing
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href": #Add links found to list of urls
                    self.urls.append(attr[1])

class ContentParser(HTMLParser): #Class with methods for extracting data from HTML
    def __init__(self): #Setting up variables [NOT GREAT]
        super().__init__()
        self.tag = "" #Store most recent tag when parsing
        self.content = "" #Store all stripped content
        self.blacklist = ["script", "style", "path"] #Tags to ignore content from
    def handle_starttag(self, tag, attrs):
        self.tag = tag
    def handle_data(self, data):
        if not data.isspace(): #If content is not whitespace add it to variable
            if not self.tag in self.blacklist:
                self.content += data + "\n"
class Page:
    def __init__(self, url):
        self.url = url
        self.loaded = False
        self.source = None
        self.content = None
        self.links = None
    def load(self, force=False, parse_content=True, parse_links=True):
        if not self.loaded or force:
            self.loaded = True
            
            url = urllib.parse.urlparse(self.url) #Parses url into an object
            if url.scheme == "http": #Use HTTP or HTTPS as appropriate
                conn = http.client.HTTPConnection(url.netloc)
            elif url.scheme == "https":
                conn = http.client.HTTPSConnection(url.netloc)
            else: #Do not process schemes other than http and https e.g. mailto:
                return None
            conn.request("GET", url.path)
            response = conn.getresponse()
            self.source = response.read().decode("utf-8", "ignore") #Store source string UTF-8 decoded [BODGE]

            if parse_content:
                parser = ContentParser()
                parser.feed(self.source)
                self.content = parser.content

            if parse_links:
                parser = LinkParser()
                parser.feed(self.source)
                absolute_urls = []
                for relative_url in parser.urls:
                    absolute_url = urllib.parse.urljoin(self.url, relative_url)
                    if urllib.parse.urlparse(absolute_url).scheme in ("http", "https"):
                        absolute_urls.append(absolute_url)
                self.links = list(dict.fromkeys(absolute_urls))

