import crawlers.burschenschaftDe as burschiDeCrawler
import crawlers.webLinks as webLinksCrawler
import json

burschis = burschiDeCrawler.get_burschi_info()
print("%s burschis collected" % len(burschis))

links_all_burschis = [] #list of dicts with all external links
print("Collecting external links for burschis.")
i = 0
for burschi in burschis:
    i += 1
    url = burschi["web_link"]
    page_links = webLinksCrawler.get_external_links(url)
    print("%s. %s links added for %s" % (i,len(page_links), url))
    burschi["external_links"] = page_links
with open("burschis.json", 'w') as out:
    out.write(json.dumps(burschis))
