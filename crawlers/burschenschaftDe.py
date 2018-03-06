import urllib.request
import json
from bs4 import BeautifulSoup
import ssl

def get_burschi_info():

    baseUrl = 'http://www.burschenschaft.de/'
    # took the hannover subpage because at the main page, the list is present twice
    domain = 'burschenschaft-in-deutschland-und-oesterreich/hannover.html'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # returns the html string of an url
    def get_html(url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.read()

    # returns a list of the subpages for the different citys
    def get_burschi_subpages(html_doc):
        result = []
        soup = BeautifulSoup(html_doc, 'html.parser')
        for a in soup.find_all('a', attrs={'class': 'list-group-item'}):
            if( a['href'] != domain):
                result.append(a['href'])
        return result

    # extracts name and web_link of each burschi on the subpage (in the city)
    # returns the result as a list of dictionarys    
    def get_data_from_subpage(html_doc):
        result = []
        link_soup = BeautifulSoup(html_doc, 'html.parser')
        # normal div around each burschi
        subpage_burschis_html = link_soup.find_all('div', attrs={'class': 'intext'})
        # special divs used sometimes to wrap burschi information, having unique ids
        special_burschis = link_soup.find_all('div', id=lambda x: x and ( any( id in x for id in ("c381","c423","c559", "c642"))))
        #add those special divs if necessary
        if special_burschis:
            subpage_burschis_html.extend(special_burschis)

        for burschi_html in subpage_burschis_html:
            burschi_info = {}
            if burschi_html.h3:
                # The burschi name is always wrapped into a h3 element
                burschi_info["name"] = burschi_html.h3.get_text()
                for paragraph in burschi_html.find_all('p', attrs={'class': 'bodytext'}):
                    if( "Netzseite" in paragraph.get_text()):
                        web_link = paragraph.find_all('a')[0]['href']
                        #sometimes the email adress is the first link
                        #its always containing javascript and we take the next one
                        if "javascript" in web_link:
                            web_link = paragraph.find_all('a')[1]['href']
                        burschi_info["web_link"] = web_link
                # identify missing links and add them "manually"
                if any(c not in burschi_info for c in ("name", "web_link")):
                    if "Burschenschaft Arminia zu Leipzig" in burschi_info["name"]:
                        burschi_info["web_link"] = "www.arminia-leipzig.de"
                result.append(burschi_info)
        return result

    start_page_html = get_html(baseUrl + domain)
    burschi_subpages = get_burschi_subpages(start_page_html)

    burschi_infos = [];
    for subpage in burschi_subpages:
        subpage_url = (baseUrl + subpage)
        subpage_html = get_html(subpage_url)
        city_info = get_data_from_subpage(subpage_html)
        if city_info:
            burschi_infos.extend(city_info)
    return burschi_infos
