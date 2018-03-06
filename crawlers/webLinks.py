import urllib.request
import json
from bs4 import BeautifulSoup
import ssl

def get_external_links(input_url):

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


 test = 1
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

    def get_next_html(url):
        #TODO: Navigate to next subpage and return html_doc
        int_links.remove(url)
        req = urllib.request.Request(url)
        int_links_checked.add(url)
        with urllib.request.urlopen( req, context=ctx) as response:
            return response.read

    def get_links(html_doc):
        #TODO: get all links and return them as a list
        return 'foo'


    int_links.add(input_url)
    #Main logic:
    # int_links and int_links_checked are sets 
    # ext_links is the object being returned at the end
    # 
    while len(int_links) > 0:
        # TODO:
        # 1. call get_links with input url
        # 2. add ext_links & int_links to their sets
        # (if ext_links already contains dict with link = some_ext_link, 
        #   increment count)
        return "bar"
    return ext_links

    #issues could be:
    #
    # - internal url could be a sub domain
    #   e.g. http://burschi.de as main url
    #       http://kontakt.burschi.de as sub url
    #   so better cut http:// or https:// before checking
    #   if a domain is internal.
