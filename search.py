import crawl
website = crawl.crawl("https://www.wikipedia.org/", 50)
searched = []

def search(term):
    x = 0
    searched = []
    while x != (len(website)-1):
        if term in website[x].term_frequency:
            searched.append(website[x])
            x += 1
        else:
            x += 1
    searched.sort(key=lambda x: x.term_frequency[term], reverse=True)
    return (searched)
