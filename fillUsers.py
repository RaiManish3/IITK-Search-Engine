import db_amend as dbA

fd=open('allUsers.txt','w')
fd.close()
fd=open('allUsers.txt','a')
y=(15,)
for y in year:
	mail_info = dbA.queryMail(y)
	for m in mail_info:
		fd.write(m[0]+'\n')