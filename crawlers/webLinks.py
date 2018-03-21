import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import ssl
import requests
import sys

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

    # returns the html string of an url
    def get_next_html(url):
        try: 
            return requests.get(url, verify=False).text
        except:
            # print("### EXCEPTION WHILE REQUESTING HTML: %s\n%s\n%s" % (sys.exc_info()[0],sys.exc_info()[1], sys.exc_info()[2]))
            print("ERROR: %s" % url)

    # def get_next_html(url):
    #     try:
    #         req = urllib.request.Req
    #         with urllib.request.urlopen(url) as response:
    #             return response.read
    #     except:
    #         try:
    #             with urllib.request.urlopen(url, context=ctx) as response:
    #                 return response.read    
    #         except:
    #             print("### EXCEPTION WHILE REQUESTING HTML: %s\n%s\n%s" % (sys.exc_info()[0],sys.exc_info()[1], sys.exc_info()[2]))
    #     #the following 

    def get_links(html_doc):
        result = []
        soup = BeautifulSoup(html_doc, 'html.parser')
        for a in soup.find_all('a'):
            link = a.get('href')
            if link != None:
                result.append(link)
        for area in soup.find_all('area'):
            link = area.get('href')
            if link != None:
                result.append(link)
        return result

    while len(int_links) > 0:
        url = int_links.pop()
        if url in int_links_checked:
            continue
        else:
            int_links_checked.add(url)
        if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".pdf"):
            continue
        html_doc = get_next_html(url)
        if html_doc == None:
            continue
        link_list = get_links(html_doc)
        if link_list == None:
            continue
        for l in link_list:
            if l.startswith('http://') or l.startswith('https://') or l.startswith('www.'):
                if parent_domain not in l:
                    check = False
                    for dict in ext_links:
                        if dict['link'] == l:
                            dict['count'] += 1
                            check = True
                    if not check:
                        ext_links.append({'link': l, 'count': 1})
                else:
                    int_links.add(l)
            else:
                int_link = urljoin(input_url, l);
                int_links.add(int_link)
    return ext_links
