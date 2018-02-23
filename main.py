import crawlers.burschenschaftDe as burschiDeCrawler
import crawlers.webLinks as webLinksCrawler

burschis = burschiDeCrawler.get_burschi_info()
for burschi in burschis:
    url = burschi.web_link
    page_links = webLinksCrawler.get_external_links()
    burschi["page_links"] = page_links

print( burschis)
