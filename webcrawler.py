import urllib.request as ul
import re
#uncomment below if working on python 2.x
#but then you need to change the student search code as well using python 2.x urllib2 instead of urllib.reqest
#from BeautifulSoup import *
from bs4 import BeautifulSoup
#import the file from different directory
import sys
sys.path.insert(0, 'Student_Search')
import st_search as ss
import web_scraper_linked as wsl

# make predictive.(i.e can handle common errors)
key = input('Enter the search query: ')
# for reg ex : we take key to be independent word
key = r'[\A\s]'+re.escape(key)+r'\s'
roll = 150001
limit_roll = 160000
url = 'http://home.iitk.ac.in/~'
#make a dictionary of all the links encountered having key
links_dic={}
max_entries = 100           #limit max entries for searches , we aren't using databses now so need to do this

while roll < limit_roll:
    while True:
        try:
            stud_data = ss.getStudentData(str(roll))
            # if program is not present as a key then we are done with this year student
            if 'Program: ' not in stud_data.keys():
                break
            user = stud_data[' E-Mail: '].split('@')[0]
        except:
            roll+=1
            continue
        end_url = url + str(user)
        #try to open the site
        try:
            data = ul.urlopen(end_url).read()
        except:
            roll+=1
            continue
        soup = BeautifulSoup(data, 'html.parser')
        #print(soup.prettify())
        #find key only if the page is made rather it just be existing there
        title_of_page = soup.title
        if title_of_page == None:
            roll+=1
            continue
        title_of_page=title_of_page.name
        if not re.search('index',title_of_page,re.IGNORECASE):
            #find all links on that page containing the key
            links_to = wsl.getRelatedList([end_url], key)
            for link_elem in links_to:
                if link_elem in links_dic.keys():
                    links_dic[link_elem]+=1
                else:
                    links_dic[link_elem]=1
        print (roll, user)
        roll+=1
    roll=((roll//10000)+1)*10000+1

print (links_dic)
#the process is rather slow, also the links on page may contain links that link back to same page so we need to avoid those.
