import urllib.request
from bs4 import BeautifulSoup

burschisWikiUrl = "https://de.wikipedia.org/wiki/Liste_der_Burschenschaften"
req = urllib.request.Request(burschisWikiUrl)
with urllib.request.urlopen(req) as response:
   html = response.read()
  

soup = BeautifulSoup(html, 'html.parser')

rows = soup.find_all('tr')

burschis = []

for row in rows:
  if( row.find('span')):
    burschis.append(row)

for burschi in burschis:
  print( burschi.prettify())
  data = burschi.find_all('td')
  for index, line in enumerate(data):
    print( str(index) + "   " + str(line.find(text=True, recursive=False)))

