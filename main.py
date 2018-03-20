import crawlers.burschenschaftDe as burschiDeCrawler
import crawlers.webLinks as webLinksCrawler

burschis = burschiDeCrawler.get_burschi_info()

links_all_burschis = [] #list of dicts with all external links

for burschi in burschis:
    url = burschi["web_link"]
    page_links = webLinksCrawler.get_external_links(url)
    print(page_links)
    #add dicts with ext links to list or increment count
    for dict in page_links:
        if dict['link'] in links_all_burschis:
            dict['count'] += 1
        else:
            links_all_burschis.append(dict)
print(links_all_burschis)
