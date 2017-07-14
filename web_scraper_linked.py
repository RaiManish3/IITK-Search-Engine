import re
import json
import urllib.request as ul
from bs4 import BeautifulSoup
import queue

import db_amend as dbA


base_url = 'http://home.iitk.ac.in/~'
OUTFILE = 'scrapedData.json'
MAX_DEPTH = 10
# hash functions have O(1) search time complexity on an average
visited = {}
iterations = 0

f=open(OUTFILE,'w')
f.close()

#although its possible to crawl quora i am not doing that here
do_not_visit_these = ['^#','facebook','linkedin','instagram','quora','twitter','google','youtube','void','oars','jpg','png','gif','pdf','mailto:','zip$','github']
DNVreg = r''+ '|'.join(do_not_visit_these)

def htmlText(soup):
    for script in soup.find_all('script'):
        script.extract()
    for style in soup.find_all('style'):
        style.extract()
    data = ' '.join(soup.get_text().strip().split())
    return data


def getValidPage():
    pass


#the arguments to be passed , url_list  and key
def scan_all_links(url_list):
    global iterations

    if url_list.empty() or iterations>MAX_DEPTH: return
    url = url_list.get()
    visited[url]=True
    print(url)

    data=''
    try:
        data = ul.urlopen(url).read()
    except:
        scan_all_links(url_list)
    soup = BeautifulSoup(data, 'html.parser')

    # get all links on this page :: all links = <a> + <iframe>
    all_links = soup.find_all('a')

    ## here try to ensure that only a valid looking url gets added to queue
    # right now gets caught in appending 'the_url' at the end of 'url'
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

    all_text = htmlText(soup)
    if url.endswith('/'):
        url = url[:-1]

    if all_text:
        tmpD = {"url":url,"pageData":all_text}
        f.write(json.dumps(tmpD)+'\n')

    iterations+=1
    scan_all_links(url_list)


if __name__ == "__main__":
    #------------------------------------------------------ all variables
    f=open(OUTFILE,'a')
    year = [15,]
    #------------------------------------------------------ all variables

    for y in year:
        mail_info = dbA.queryMail(y)
        for (user,) in mail_info:
            iterations = 0
            #find all links on that page
            #links_to makes more sense if it is Priority queue
            q = queue.Queue()
            q.put(base_url+user)
            scan_all_links(q)
            print(user)
    f.close()
