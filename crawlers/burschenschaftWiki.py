import urllib.request
import json
from bs4 import BeautifulSoup

burschisWikiUrl = "https://de.wikipedia.org/wiki/Liste_der_Burschenschaften"
baseUrl = "https://de.wikipedia.org"
req = urllib.request.Request(burschisWikiUrl)
with urllib.request.urlopen(req) as response:
   html = response.read()
  

soup = BeautifulSoup(html, 'html.parser')

rows = soup.find_all('tr')

burschis = []

burschiDict = {}

for row in rows:
  if( row.find('span')):
    burschis.append(row)

for baseIndex, burschi in enumerate(burschis):
  data = burschi.find_all('td', recursive=False)

  burschiDict[baseIndex] = {}

  for propIndex, line in enumerate(data):

    print( line)
    lineTexts = []
    link = ""

    if(line.find('a') != None):
      lineTexts = line.find('a').find_all(text=True, recursive=False)
    else:
      lineTexts = line.find_all(text=True, recursive=False)

    if(line.find('img') != None):
      link = "https:" + line.find('img')['src']

    mockText = ""  
    if(len(lineTexts) > 0):
      mockText = lineTexts[-1]
    else:
      mockText = ""

    text = mockText.replace('\n', '')
    print( "%s:  %s" % (propIndex, text))

    dictPos = burschiDict[baseIndex]
    if propIndex == 0:
      dictPos['title'] = text
    elif propIndex == 1:
      if('location' in dictPos):
        dictPos['location']['city'] = text
      else:
        dictPos['location'] = {'city': text}
    elif propIndex == 2:
      dictPos['year'] = text
    elif propIndex == 3:
      dictPos['colors'] = text
    elif propIndex == 4:
      dictPos['union'] = text
    elif propIndex == 5:
      dictPos['syndicate'] = text
    elif propIndex == 6:
      dictPos['incorporation'] = text
    elif propIndex == 7:
      if('logo' in dictPos):
        dictPos['logo']['link'] = link
      else:
        dictPos['logo'] = { 'link': link}
    elif propIndex == 8:
      if('weirdLogo' in dictPos):
        dictPos['weirdLogo']['link'] = link
      else:
        dictPos['weirdLogo'] = { 'link': link}
    elif propIndex == 9:
      dictPos['striking'] = text
    elif propIndex == 10:
      dictPos['status'] = text

  print( "\n\n\n")
print( "%s \n %s" % (json.dumps(burschiDict, indent=4, ensure_ascii=False),10) )
