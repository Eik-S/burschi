import requests
from bs4 import BeautifulSoup

burschisUrl = "http://www.burschenschaft.de/burschenschaft-in-deutschland-und-oesterreich.html"
burschisWikiUrl = "www.de.wikipedia.org/wiki/Liste_der_Burschenschaften"

data = requests.get( burschisUrl, stream=True)

result = "";

for line in data.iter_lines():
  if line: 
    result += line;
  

soup = BeautifulSoup( result, 'html.parser')

print soup.
