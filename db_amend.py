import sqlite3
import sys
sys.path.insert(0, 'Student_Search')
import st_search as ss

# Create table
table_heads = """CREATE TABLE iitk_students(rollno int primary key, name text, program varchar(100), department varchar(100),hostel varchar(100), email varchar(100), gender varchar(100), bloodGroup varchar(100), country varchar(100),imageUrl varchar(100))"""
roll = 160001
lim = 170000
should_keys = ['Roll No: ','Name: ','Program: ','Department: ','Hostel Info: ',' E-Mail: ',' Gender:',' Blood Group:',' CountryOfOrigin:','image']

def createTable():
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute(table_heads)
    conn.close()

def updateTable(roll):
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    while roll<lim:
        si = ss.getStudentData(roll)
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
    c.execute("SELECT rollno, email FROM iitk_students WHERE rollno LIKE ?",(year,))
    data = c.fetchall()
    conn.close()
    return data


#print(queryStudent(name=input('Enter name: '),year=input('Enter year: ')))
