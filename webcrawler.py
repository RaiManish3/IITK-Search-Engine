## currently implemented for python 3.x
import urllib.request as ul
import re
from bs4 import BeautifulSoup
#import the file from different directory
import sys
sys.path.insert(0, 'Student_Search')

import queue

#import st_search as ss
import web_scraper_linked as wsl
import db_amend as dbA


base_url = 'http://home.iitk.ac.in/~'

def searchIITK(year):

    #------------------------------------------------------ all variables

    # make predictive.(i.e can handle common errors)
    key = input('Enter the search query: ')
    # for reg ex : we take key to be independent word
    key = re.escape(key)
    #make a dictionary of all the links encountered having key
    links_dic={}

    #------------------------------------------------------ all variables

    mail_info = dbA.queryMail(year)
    for (user,) in mail_info:
        #find all links on that page containing the key
        #links_to makes more sense if it is Priority queue
        q = queue.Queue()
        q.put(base_url+user)
        links_to = wsl.getRelatedList(q, key)
        #check for hits
        for link_elem in links_to:
            if link_elem in links_dic.keys():
                links_dic[link_elem]+=1
            else:
                links_dic[link_elem]=1
        print(user)

    print(links_dic)

searchIITK(15)
