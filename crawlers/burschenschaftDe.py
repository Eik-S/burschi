import urllib.request
from bs4 import BeautifulSoup

burschisUrl = "http://www.burschenschaft.de/burschenschaft-in-deutschland-und-oesterreich.html"
burschisWikiUrl = "www.de.wikipedia.org/wiki/Liste_der_Burschenschaften"
req = urllib.request.Request(burschisUrl)
with urllib.request.urlopen(req) as response:
   html = response.read()
  

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())
