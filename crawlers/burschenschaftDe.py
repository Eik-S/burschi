import urllib.request
from bs4 import BeautifulSoup


def log(string, fname):
    with open('../log/' + fname + '.log', 'a+') as logfile:
        logfile.write(string + '\n')


def get_html(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return response.read()


def get_all_links_with_class_list_group_item(html_doc):
    result = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    for a in soup.find_all('a', attrs={'class': 'list-group-item'}):
        result.append(a['href'])
    return result


def get_all_links_from_content_div(html_doc):
    result = []
    link_soup = BeautifulSoup(html_doc, 'html.parser')
    for div in link_soup.find_all('div', attrs={'class': 'content'}):
        for a in div.find_all('a'):
            result.append(a['href'])
    return result


visited_links = []

baseUrl = 'http://www.burschenschaft.de/'
domain = 'burschenschaft-in-deutschland-und-oesterreich.html'

stadt_page = get_html(baseUrl + domain)

staedte_links = get_all_links_with_class_list_group_item(stadt_page)
visited_link = staedte_links


for stadt_link in staedte_links:
    stadt_page = get_html(baseUrl + stadt_link)
    for content_link in get_all_links_from_content_div(stadt_page):
        if content_link in visited_links:
            continue
        elif content_link not in visited_links:
            visited_links.append(content_link)
            log(content_link, 'content_links')






