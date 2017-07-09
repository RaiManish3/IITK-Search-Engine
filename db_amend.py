import sqlite3
import sys
sys.path.insert(0, 'Student_Search')
import st_search as ss

## currently implemented for python 3.x
import urllib.request as ul
import re
from bs4 import BeautifulSoup

roll = 13001
lim = 14000
url = 'http://home.iitk.ac.in/~'
should_keys = ['Roll No: ','Name: ','Program: ','Department: ','Hostel Info: ',' E-Mail: ',' Gender:',' Blood Group:',' CountryOfOrigin:','image']


def generateValidPage(year):
    st_info = queryYear(year)
    lst = []
    for (roll,mail) in st_info:
        user = mail.split('@')[0]
        end_url = url + str(user)

        #try to open the site
        try:
            data = ul.urlopen(end_url).read()
        except:
            continue
        soup = BeautifulSoup(data, 'html.parser')

        # Ensure that the page has been setup by the developer
        title_of_page = soup.title
        if title_of_page == None:
            continue
        title_of_page=str(title_of_page.string)
        if not re.search('index',title_of_page,re.IGNORECASE):
            lst.append((roll,user))
    return lst

def createStudentTable():
    # Create table
    table_heads = """CREATE TABLE iitk_students(rollno int primary key, name text, program varchar(100), department varchar(100),hostel varchar(100), email varchar(100), gender varchar(100), bloodGroup varchar(100), country varchar(100),imageUrl varchar(100))"""
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute(table_heads)
    conn.close()

def validWebPageTable():
    table_heads = """CREATE TABLE valid_mails(rollno int primary key, username varchar(20))"""
    drop_table = """DROP TABLE valid_mails"""
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute(drop_table)
    c.execute(table_heads)
    conn.close()

def updateStudentTable(roll):
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    while roll<lim:
        si = ss.getStudentData(roll)
        #print(si)
        if 'Program: ' not in si.keys():
            break
        lk={}
        for k in should_keys:
            if k not in si.keys():
                lk[k]=''
            else:
                lk[k]=' '.join(si[k].strip().split())
        print(lk['Roll No: '])
        c.execute("SELECT rollno FROM iitk_students WHERE rollno = ?", (roll,))
        data = c.fetchall()
        if len(data)==0:
            c.execute("INSERT INTO iitk_students VALUES(?,?,?,?,?,?,?,?,?,?)", (int(lk['Roll No: ']),lk['Name: '], lk['Program: '], lk['Department: '], lk['Hostel Info: '], lk[' E-Mail: '], lk[' Gender:'], lk[' Blood Group:'], lk[' CountryOfOrigin:'], lk['image']))
            conn.commit()
        roll+=1
    conn.close()


def updateMailTable():
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    years = [13,14,15,16]
    for y in years:
        # filter out those users which have a webpage
        mailPage = generateValidPage(y)
        for (rollno, user) in mailPage:
            print(rollno,user)
            c.execute("SELECT rollno FROM valid_mails WHERE rollno = ?", (rollno,))
            data = c.fetchall()
            if len(data)==0:
                print("inserting")
                c.execute("INSERT into valid_mails VALUES(?,?)", (rollno,user))
            else:
                print("updating")
                c.execute("UPDATE valid_mails SET rollno=? , username=?", (rollno,user))
            conn.commit()

    conn.close()



def queryStudent(name='', year=None, gender='', program='', hall='', department='', bg=None):
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    #make
    name='%'+name.strip()+'%'
    rollno=''
    if year:
        rollno=year[1:].strip()+'%'
    else:
        rollno='%'
    program='%'+program.strip()+'%'
    department='%'+department+'%'
    hall='%'+hall.strip()+'%'
    if not bg:
        bg = '%'
    if not gender:
        gender = '%'
    c.execute("SELECT rollno, name FROM iitk_students WHERE name LIKE ? and rollno LIKE ? and gender LIKE ? and program LIKE ? and hostel LIKE ? and department LIKE ? and bloodGroup LIKE ?",(name,rollno,gender,program,hall,department, bg))
    data = c.fetchall()
    conn.close()
    return data

def queryYear(year):
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    year=str(year)+'%'
    c.execute("SELECT rollno, email FROM iitk_students WHERE rollno LIKE ? and email IS NOT NULL AND TRIM(email) <> '' ",(year,))
    data = c.fetchall()
    conn.close()
    return data

def queryMail(year):
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    year=str(year)+'%'
    c.execute("SELECT username FROM valid_mails where rollno LIKE ?",(year,))
    data = c.fetchall()
    conn.close()
    return data

