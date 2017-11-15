import urllib.request
from bs4 import BeautifulSoup

baseUrl = 'http://www.burschenschaft.de/'
domain = 'burschenschaft-in-deutschland-und-oesterreich.html'

req = urllib.request.Request(baseUrl + domain)
with urllib.request.urlopen(req) as response:
    html = response.read()

soup = BeautifulSoup(html, 'html.parser')

cityPages = []

for link in soup.find_all('a', attrs={'class': 'list-group-item'}):
    href = link['href']
    print(href)
    req = urllib.request.Request(baseUrl + href)
    with urllib.request.urlopen(req) as response:
        cityPages.append(response.read)





