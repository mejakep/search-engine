import pages

crawled = []
to_be_crawled = ["https://www.whsb.essex.sch.uk"]
while len(crawled) < 10:
    start = pages.Page(to_be_crawled[0])
    start.load()
    to_be_crawled += start.links
    to_be_crawled = list(dict.fromkeys(to_be_crawled))
    crawled.append(start)
    to_be_crawled.pop(0)
