import pages
from random import randint

def crawl(website, depth = 10):
    crawled = []
    to_be_crawled = [website]
    while len(crawled) < depth:
        x = randint(0, len(to_be_crawled))
        start = pages.Page(to_be_crawled.pop(x))
        start.load()
        to_be_crawled += start.links
        to_be_crawled = list(dict.fromkeys(to_be_crawled))
        crawled.append(start)
    return (crawled)