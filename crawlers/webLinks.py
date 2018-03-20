import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import ssl
import requests

def get_external_links(input_url):
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    if not input_url.startswith('http://') and not input_url.startswith('https://'):
        input_url = 'http://' + input_url
        
    #cut parent domain from input url:
    parent_domain = urlparse(input_url).netloc
    if parent_domain.startswith('www.'):
        parent_domain = parent_domain[4:]
    

    int_links = set()
    int_links_checked = set()
    ext_links = [
        #just some example data to know the structure
        #{
        #    "link": "http://nursonenaziseite.de",
        #    "count": 1
        #},
        #{
        #    "link": "http://freiheitehreblablabla.de",
        #    "count": 3
        #}
    ]
    
    int_links.add(input_url)

    def get_next_html(url):
        req = requests.get(url).text
        return req
        #the following 
        #with urllib.request.urlopen(req, context=ctx) as response:
         #   return response.read    

    def get_links(html_doc):
        result = []
        soup = BeautifulSoup(html_doc, 'html.parser')
        for a in soup.find_all('a'):
            if a.get('href') != None:
                result.append(a)
            else:
                continue
        for area in soup.find_all('area'):
            if area.get('href') != None:
                result.append(area)
            else:
                continue
        return result

    while len(int_links) > 0:
            try:
                    url = int_links.pop()
                    int_links_checked.add(url)
                    if get_next_html(url) != None:
                        html_doc = get_next_html(url)
                        if get_links(html_doc) != None:
                            link_list = get_links(html_doc)
                            
                            #decide if link in output of get_links is internal or external
                            #append internal links to int_links, for external link
                            #create new dict in ext_links or increment count if link is 
                            #already present
                            for link in link_list:
                                l = link.get('href')
                                if l not in int_links_checked:
                                    if l.startswith('http://') or l.startswith('https://') or l.startswith('www.'):
                                        if parent_domain not in l:
                                            check = False
                                            for dict in ext_links:
                                                if dict['link'] == l:
                                                    dict['count'] =+ 1
                                                    check = True
                                            if not check:
                                                ext_links.append({'link': l, 'count': 1})
                                        elif l.count('http') > 1 or l.count('www') > 1:
                                            check = False
                                            for dict in ext_links:
                                                if dict['link'] == l:
                                                    dict['count'] =+ 1
                                                    check = True
                                            if not check:
                                                    ext_links.append({'link': l, 'count': 1})
                                        else:
                                            int_links.add(l)
                                    elif not l.startswith('http://') and not l.startswith('https://')  and not l.startswith('www.'):
                                        int_links.add(urljoin(input_url, l))
                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue
            except:
                pass
            
            return ext_links
