import crawl
website = crawl.crawl("https://www.wikipedia.org/", 100)

def search(term):
    x = 0
    result = []
    while x != (len(website)-1):
        if term in website[x].term_frequency:
            result.append(website[x])
            x += 1
        else:
            x += 1
    return (result)
    #for page in website:
        #if (term) in page.term_frequency:
            #result = page.term_frequency[term]
            #return (result)

search("the")
