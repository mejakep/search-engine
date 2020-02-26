import pages

#Example:
start = pages.Page("https://www.whsb.essex.sch.uk")
print("start:    ", start)
print("    start.url:    ", start.url)
print("    start.loaded:    ", start.loaded)
print("    start.source:    ", start.source)
print("    start.content:    ", start.content)
print("    start.links:    ", start.links)

print("\nstart.load()\n")
start.load()

print("start:    ", start)
print("    start.url:    ", start.url)
print("    start.loaded:    ", start.loaded)
print("    start.source:    ", start.source)
print("    start.content:    ", start.content)
print("    start.links:    ", start.links)

#End example
import urllib.parse

webpages = {}
start = pages.Page("https://www.whsb.essex.sch.uk")
webpages[start.url] = start
while len(webpages) < 200:
    print("crawling")
    print(len(webpages))
    for url in list(webpages.keys()):
        page = webpages[url]
        if not page.loaded:
            page.load()
        for link in page.links:
            if not link in webpages.keys():
                webpages[link] = pages.Page(link)
