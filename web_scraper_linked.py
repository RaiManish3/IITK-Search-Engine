import re
import urllib.request as ul
from bs4 import BeautifulSoup
import queue

MAX_DEPTH = 10
ln_with_key = []
iterations = 0
#the arguments to be passed , url_list  and key
def scan_all_links(url_list,key):
    global iterations
    if url_list.empty() or iterations>MAX_DEPTH: return
    url = url_list.get()
    #del url_list[0]
    data=''
    iterations+=1
    try:
        data = ul.urlopen(url).read()
    except:
        scan_all_links(url_list,key)
    soup = BeautifulSoup(data, 'html.parser')
    #although its possible to crawl qoura i am not doing that here
    do_not_visit_these = ['#','facebook','linkedin','plus.google','instagram','quora']
    #get all links on this page
    all_links = soup.find_all('a')
    for lk in all_links:
        flag2 = False
        the_url = lk.get('href')
        if the_url == None or not the_url:
            continue
        for dn in do_not_visit_these:
            if re.search(dn,the_url,re.IGNORECASE):
                flag2=True
                break
        if flag2: continue
        url_list.put(the_url)

    #check if the current 'url' contains the key
    all_text = soup.get_text()
    if re.search(key, all_text, re.IGNORECASE):
        if url.endswith('/'):
            url = url[:-1]
        ln_with_key.append(url)
    scan_all_links(url_list,key)

def getRelatedList(url_list, key):
    global iterations, ln_with_key
    iterations = 0
    ln_with_key = []
    scan_all_links(url_list,key)
    return list(set(ln_with_key))[:]

