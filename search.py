import crawl
website = crawl.crawl("https://www.whsb.essex.sch.uk", 10)
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
    for page in searched:
        print(page.url)
    return(searched)