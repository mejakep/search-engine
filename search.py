import crawl
website = crawl.crawl("https://www.whsb.essex.sch.uk", 10)
result = []

def search(term):
    for page in website:
        if (term) in page.term_frequency:
            result = page.term_frequency[term]
            return (result)

search("the")