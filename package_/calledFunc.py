'''
Created on Dec 8, 2017

@author: shrbhatt
'''
import re
import pymysql


db = pymysql.connect("shrbhatt-wx-3","root","root","Enablyzer_Ppro")
# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
#
cursor.execute("DROP TABLE IF EXISTS codeCalledfunc1")
sql_qry = """CREATE TABLE codeCalledfunc1(CodeCalledFuncId bigint(20) not null auto_increment,
   CodeFileId bigint(20), CodeDeclaredFuncId bigint(20),Type varchar(100), declared_func varchar(1000),Called_func varchar(1000), PRIMARY KEY (`CodeCalledFuncId`))ENGINE=InnoDB AUTO_INCREMENT=10123 DEFAULT CHARSET=utf8"""
cursor.execute (sql_qry)

sql_qry2="""SELECT CodeDeclaredFuncId,CodeFileId,type,declared_func,begin,end,Code_content from codedeclaredfunc"""
cursor.execute(sql_qry2)
files = cursor.fetchall()
print(len(files))
sql_qry3="""INSERT INTO codeCalledfunc1(Codefileid,CodeDeclaredFuncId,type,declared_func,Called_func) VALUES(%s,%s,%s,%s,%s)"""
for f in files:
    fileid=f[1]
    funcid=f[0]
    typ=f[2]
    func=f[3]
    beg=f[4]
    end=f[5]
    #print(func,beg,end,id)
    content=f[6].split('\n');
    for i in range(beg+1,end):
        called_func=re.findall('[A-Za-z_][A-Za-z0-9_]*\([^\)]*\)',content[i-1])
            #print(called_func)
        ln=len(called_func)
        while ln:
            cf=called_func[ln-1].split('(')
            for j in range(0,len(cf)-1):
                #print(cf[j])
                cf1=re.findall('[A-Za-z_][A-Za-z0-9_]*',cf[j])
                if cf1:
                    cf[j]=cf1[len(cf1)-1].strip()
                    
                    #print(cf[j])
                    if cf[j]=='if' or cf[j]=='while' or cf[j]=='for' or cf[j]=='switch' or cf[j]=='catch' or not re.search('[a-zA-Z]', cf[j]):
                        continue
                    cursor.execute(sql_qry3,(fileid,funcid,typ,func,cf[j]))
                    db.commit()
            ln=ln-1
            
