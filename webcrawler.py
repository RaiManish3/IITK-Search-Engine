import urllib.request as ul
import re
#uncomment below if working on python 2.x
#but then you need to change the student search code as well using python 2.x urllib2 instead of urllib.reqest
#from BeautifulSoup import *
from bs4 import BeautifulSoup
#import the file from different directory
import sys
sys.path.insert(0, 'Student_Search')

import queue

#import st_search as ss
import web_scraper_linked as wsl
import db_amend as dbA

# make predictive.(i.e can handle common errors)
key = input('Enter the search query: ')
# for reg ex : we take key to be independent word
key = r'[\A\s]'+re.escape(key)+r'\s'
url = 'http://home.iitk.ac.in/~'
#make a dictionary of all the links encountered having key
links_dic={}
max_entries = 100           #limit max entries for searches , we aren't using databses now so need to do this

#while roll < limit_roll:
def queryOnYear(year):
    st_info = dbA.queryYear(year)
    for (roll,mail) in st_info:
        user = mail.split('@')[0]
        end_url = url + str(user)
        #try to open the site
        try:
            data = ul.urlopen(end_url).read()
        except:
            continue
        soup = BeautifulSoup(data, 'html.parser')
        #print(soup.prettify())
        #find key only if the page is made rather it just be existing there
        title_of_page = soup.title
        if title_of_page == None:
            continue
        title_of_page=title_of_page.name
        if not re.search('index',title_of_page,re.IGNORECASE):
            #find all links on that page containing the key
            #links_to makes more sense if it is Priority queue
            q = queue.Queue()
            q.put(end_url)
            links_to = wsl.getRelatedList(q, key)
            #check for hits
            for link_elem in links_to:
                if link_elem in links_dic.keys():
                    links_dic[link_elem]+=1
                else:
                    links_dic[link_elem]=1
        print(roll,user)

queryOnYear(15)
print (links_dic)
