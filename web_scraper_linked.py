import re
import urllib.request as ul
from bs4 import BeautifulSoup
import queue

MAX_DEPTH = 10
ln_with_key = []
visited = []
iterations = 0

#although its possible to crawl qoura i am not doing that here
do_not_visit_these = ['#$','facebook','linkedin','plus.google','instagram','quora','twitter','google']
DNVreg = r''+ '|'.join(do_not_visit_these)

def pageData(soup):
    texts = soup.findAll(text=True)

    """
    try:
        tmp = soup.find('iframe')['src']
        print(tmp)
    except:
        pass
    """

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True

    visible_texts = filter(visible, texts)
    return '\n'.join(' '.join(list(visible_texts)).splitlines())


#the arguments to be passed , url_list  and key
def scan_all_links(url_list,key):
    global iterations
    if url_list.empty() or iterations>MAX_DEPTH: return
    url = url_list.get()
    visited.append(url)
    data=''
    iterations+=1
    try:
        data = ul.urlopen(url).read()
    except:
        scan_all_links(url_list,key)
    soup = BeautifulSoup(data, 'html.parser')

    # get all links on this page :: all links = <a> + <iframe>
    all_links = soup.find_all('a')

    for lk in all_links:
        the_url = lk.get('href')
        if not the_url:
            continue
        if re.search(DNVreg,the_url,re.IGNORECASE):
            continue
        if the_url not in visited:
            url_list.put(the_url)

    #check if the current 'url' contains the key
    all_text = pageData(soup)
    if re.search(key, all_text, re.IGNORECASE):
        if url.endswith('/'):
            url = url[:-1]
        ln_with_key.append(url)
    scan_all_links(url_list,key)

def getRelatedList(url_list, key):
    global iterations, ln_with_key, visited
    iterations = 0
    ln_with_key = []
    visited = []
    scan_all_links(url_list,key)
    return list(set(ln_with_key))[:]

