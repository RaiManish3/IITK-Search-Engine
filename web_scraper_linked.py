import re
import json
import urllib.request as ul
from bs4 import BeautifulSoup
import queue

import db_amend as dbA


base_url = 'http://home.iitk.ac.in/~'
OUTFILE = 'tmp.json'
MAX_DEPTH = 10
visited = []
iterations = 0

f=open(OUTFILE,'w')
f.close()

#although its possible to crawl quora i am not doing that here
do_not_visit_these = ['^#','facebook','linkedin','instagram','quora','twitter','google','youtube','void','oars','jpg','png','gif','pdf','mailto:','zip$','github']
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
    strx = ' '.join(list(visible_texts))
    strx = re.sub(r'\s',r' ', strx)
    return ' '.join(strx.split())


#the arguments to be passed , url_list  and key
def scan_all_links(url_list):
    global iterations

    if url_list.empty() or iterations>MAX_DEPTH: return
    url = url_list.get()
    visited.append(url)
    print(url)

    data=''
    try:
        data = ul.urlopen(url).read()
    except:
        scan_all_links(url_list)
    soup = BeautifulSoup(data, 'html.parser')

    # get all links on this page :: all links = <a> + <iframe>
    all_links = soup.find_all('a')

    for lk in all_links:
        the_url = lk.get('href')
        if not the_url:
            continue
        if re.search(DNVreg,the_url,re.IGNORECASE):
            continue

        if 'http' not in the_url:
            if 'www' not in the_url:
                if url.endswith('.html'): continue
                elif the_url[0]!='/' and url[-1]!='/': the_url=url+'/'+the_url
                else: the_url=url+the_url
            else:
                the_url='http:'+the_url
        if the_url not in visited:
            url_list.put(the_url)

    all_text = pageData(soup)
    if url.endswith('/'):
        url = url[:-1]

    if all_text:
        tmpD = {"url":url,"pageData":all_text}
        f.write(json.dumps(tmpD)+'\n')

    iterations+=1
    scan_all_links(url_list)


if __name__ == "__main__":
    global iterations

    #------------------------------------------------------ all variables
    f=open(OUTFILE,'a')
    year = 15
    #------------------------------------------------------ all variables

    mail_info = dbA.queryMail(year)
    for (user,) in mail_info:
        iterations = 0
        #find all links on that page
        #links_to makes more sense if it is Priority queue
        q = queue.Queue()
        q.put(base_url+user)
        scan_all_links(q)
        print(user)
    f.close()
