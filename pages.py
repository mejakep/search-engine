import http.client #Used to make HTTP requests for a webpage
from html.parser import HTMLParser #Used to 'parse' the HTML to look for links
import urllib.parse #Used to parse URL components
from math import log #Used for the Term-Frequency algorithm


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
    def __init__(self, url): #Setting up variables
        self.url = url
        self.loaded = False
        self.source = None
        self.content = None
        self.links = None
        self.term_frequency = None
    def load(self, force=False, parse_content=True, parse_links=True): #Fetches and process webpage
        if not self.loaded or force: #Will not load if loaded is True unless force is also True
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

            if parse_content: #Runs source code through parser to extract content
                parser = ContentParser() #Uses methods defined in ContentParser class to detect content
                parser.feed(self.source)
                self.content = parser.content

                terms = self.content.lower().split() #Split the content into a list of all words IN LOWERCASE
                self.term_frequency = dict.fromkeys(terms, 0) #Creates a key in the term_frequency for each unique term
                for term in self.term_frequency: #For each term count how many times it appears
                    self.term_frequency[term] = terms.count(term)
                for term in self.term_frequency: #Apply log algorithm on each term's frequency
                    self.term_frequency[term] = log(1 + self.term_frequency[term])
                

            if parse_links: #Runs source code through parser to extract links
                parser = LinkParser() #Uses methods defined in LinkParser class to detect <a> tags and extract the URLs from them
                parser.feed(self.source)
                absolute_urls = []
                for relative_url in parser.urls: #Convert all URLs to absolute URLs
                    absolute_url = urllib.parse.urljoin(self.url, relative_url)
                    if urllib.parse.urlparse(absolute_url).scheme in ("http", "https"):
                        absolute_urls.append(absolute_url) #Only include http and https URLs i.e. no mailto:// or ftp:// links
                self.links = list(dict.fromkeys(absolute_urls)) #Remove any duplicate links

save_prefix = "data/"
import json
from hashlib import md5

class SavedPage:
    def __init__(self, url): #Setting up variables
        self.url = url
        self.loaded = False
        self.file = None
    def load(self, force=False, parse_content=True, parse_links=True): #Fetches and process webpage
        if not self.loaded or force: #Will not load if loaded is True unless force is also True
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
            source = response.read().decode("utf-8", "ignore") #Store source string UTF-8 decoded [BODGE]

            if parse_content: #Runs source code through parser to extract content
                parser = ContentParser() #Uses methods defined in ContentParser class to detect content
                parser.feed(source)
                content = parser.content

                terms = content.lower().split() #Split the content into a list of all words IN LOWERCASE
                term_frequency = dict.fromkeys(terms, 0) #Creates a key in the term_frequency for each unique term
                for term in term_frequency: #For each term count how many times it appears
                    term_frequency[term] = terms.count(term)
                for term in term_frequency: #Apply log algorithm on each term's frequency
                    term_frequency[term] = log(1 + term_frequency[term])
                

            if parse_links: #Runs source code through parser to extract links
                parser = LinkParser() #Uses methods defined in LinkParser class to detect <a> tags and extract the URLs from them
                parser.feed(source)
                absolute_urls = []
                for relative_url in parser.urls: #Convert all URLs to absolute URLs
                    absolute_url = urllib.parse.urljoin(self.url, relative_url)
                    if urllib.parse.urlparse(absolute_url).scheme in ("http", "https"):
                        absolute_urls.append(absolute_url) #Only include http and https URLs i.e. no mailto:// or ftp:// links
                links = list(dict.fromkeys(absolute_urls)) #Remove any duplicate links

            f = open(save_prefix+md5(self.url.encode()).hexdigest(), "w")
            f.write({"source":source,"content":content,"links":links,"term_frequency":term_frequency})
            f.close()
            self.file = save_prefix+self.url
