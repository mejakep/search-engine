import pages #imports the pages module
from random import randint #imports the randint module for rng

def crawl(website, depth = 10): #website = the link you want to start the crawl from, depth = how many pages you want crawl
    crawled = [] #a list which holds the links the crawl function has already visited
    crawled_urls = []
    to_be_crawled = [website] #a list which holds the links that have not yet been explored from the sites that have been crawled
    while len(crawled) < depth:
        x = randint(0, (len(to_be_crawled)-1)) #rng for fair distribution of crawling
        if not to_be_crawled[x] in crawled_urls: #sees if the url has already been crawled
            try:
                start = pages.Page(to_be_crawled.pop(x)) #calls the Page function to turn the link selected by the rng in the to_be_crawled list into an object that can have its HTML extracted (see pages.py)
                crawled_urls.append(start.url) #adds site to the crawled_urls list
                start.load() #calls the load.() function to extect the HTML and links on that page
                to_be_crawled += start.links #adds the links found on the current page to the to_be_crawled list for future crawling
                to_be_crawled = list(dict.fromkeys(to_be_crawled)) # removes dupes in to_be_crawled
                crawled.append(start) #after all links have been explored, the current site is added to the crawled list
                if len(crawled)%10 == 0:
                    print(len(crawled))
            except:
                pass
        else:
            to_be_crawled.pop(x) #deletes site on to_be_crawled without crawling again
    return (crawled)
