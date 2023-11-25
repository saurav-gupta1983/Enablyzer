'''
Created on Dec 8, 2017

@author: shrbhatt
'''

import os
import re
import pymysql
import chardet
import traceback

db = pymysql.connect("shrbhatt-wx-3","root","root","Enablyzer_Ppro")
# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
#
cursor.execute("DROP TABLE IF EXISTS codeCalledfunc")

cursor.execute("DROP TABLE IF EXISTS codedeclaredfunc")
sql_qry= """CREATE TABLE codedeclaredfunc(`codedeclaredfuncid` bigint(20) NOT NULL AUTO_INCREMENT,
                                           `CodeFileid` BIGINT(20), 
                                           `Code_file` varchar(1000), 
                                           `Declared_func` varchar(1000),
                                           `Type` varchar(100) DEFAULT NULL,
                                           `begin` INT, 
                                           `end` INT, 
                                           `Code_content` LONGTEXT, 
                                           `Remarks` LONGTEXT,
                                           PRIMARY KEY (`codedeclaredfuncid`)) ENGINE=InnoDB AUTO_INCREMENT=111011 DEFAULT CHARSET=utf8"""
cursor.execute (sql_qry)

sql_qry1="""SELECT SourceId,SourceFilePath,Type FROM SourceFiles where (Type='Code' or (Type='UserDefined_Header' and SourceFilePath like '%.hpp'))"""
cursor.execute(sql_qry1)
files = cursor.fetchall()
sql_qry2="""INSERT INTO codedeclaredfunc(CodeFileid,Code_file,type,Declared_func,begin,end,Code_content,remarks) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
sql_qry3="""SELECT codedeclaredfuncid from codedeclaredfunc where codefileid=%s and declared_func=%s and begin=%s and end=%s"""
sql_qry4="""INSERT INTO codeCalledfunc(Codefileid,CodeDeclaredFuncId,type,declared_func,Called_func) VALUES(%s,%s,%s,%s,%s)"""
for f in files:
    
        cnt=0;
        scope=[]
        cflist=[]
        prev_st=''
        fname='temp.txt'
        file = open(fname,'w') 
        file.close()
        fileid=f[0]
        filepath=f[1]
        typ=f[2]
        #print(fid)
        flag=0;
        rawdata=open(filepath,"rb").read()
        result=chardet.detect(rawdata)
        #print(result)
        with open(filepath, encoding=result['encoding'],errors="surrogateescape") as fin:
            with open(fname, "w",encoding=result['encoding'],errors="surrogateescape") as fout:
                for line in fin:
                    if not line.strip():
                        continue
                    line = re.sub("//.*",'',line)
                    if '/*' in line:
                        line=line.replace('/*','\n/*\n')
                    if '*/' in line:
                        line=line.replace('*/','\n*/\n')
                    line = re.sub("\s+\(", "(", line)
                    fout.write(line.replace('{', '\n{\n'))
            fout.close()
        fin.close()
        with open(fname,'r+',encoding=result['encoding'],errors="surrogateescape") as fin:
            lines = list(line for line in (l.strip() for l in fin) if line)
        fin.close()
        lines_f=[]
        tmp=''
        sb=0
        flag=0
        fout=open(fname,'w+',encoding=result['encoding'],errors="surrogateescape")
        for l in lines:
            l=l.strip()
            if '/*' in l:
                flag=1
            if '*/' in l:
                flag=0
                continue;
            if flag:
                continue; 
            sb+=l.count('(');
            sb-=l.count(')');
            tmp+=l;
            if not sb:
                lines_f.append(tmp)
                tmp=''   
        del lines
        for l in lines_f:
            fout.write(l)
            fout.write('\n')
        fout.close()
        flag=0
        pre=-1
        beg=-1;
        remarks=''
        hardcodedmn_jan=hardcodedmn_sep=hardcodedmn_dec=0
        hardcodeddy_mon=hardcodeddy_wed=hardcodeddy_fri=0
        frmtm=frmtd=frmty=frmtmm=frmtdd=frmtyy=0
        for i,l in enumerate(lines_f):
            if re.search('[^A-Z\^a-z](?i)Mon', l):
                hardcodeddy_mon=1
            if re.search('[^A-Z\^a-z](?i)Wed', l):
                hardcodeddy_wed=1
            if re.search('[^A-Z\^a-z](?i)Fri', l):
                hardcodeddy_fri=1
            if re.search('[^A-Z\^a-z](?i)Jan', l):
                hardcodedmn_jan=1
            if re.search('[^A-Z\^a-z](?i)Sep', l):
                hardcodedmn_sep=1
            if re.search('[^A-Z\^a-z](?i)Dec', l):
                hardcodedmn_dec=1
            if re.search('%y', l) or re.search('%Y', l):
                frmty=1
            if re.search('%b', l) or re.search('%h', l) or re.search('%B', l):
                frmtm=1
            if re.search('%d', l):
                frmtd=1
            if re.search('[^A-Z\^a-z](?i)YY', l):
                frmtyy=1
            if re.search('[^A-Z\^a-z](?i)MM', l):
                frmtmm=1
            if re.search('[^A-Z\^a-z](?i)DD', l):
                frmtdd=1
            
            if ')' in l and '(' in l:
                pre=i;
                prev_st=lines_f[i-1].strip()
            called_func=re.findall('[A-Za-z_][A-Za-z0-9_]*\([^\)]*\)',lines_f[i-1])
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
                        if cnt>0:
                            cflist.append(cf[j])
                    #cursor.execute(sql_qry3,(fileid,'',typ,func,'')
                    #db.commit()
                ln=ln-1
            if '{' in l:          
                if cnt==0:
                    if i==pre+1 or '#endif' in prev_st or prev_st=='do' or prev_st=='while' or prev_st=='if' or prev_st=='for':
                        beg=pre+1
                        cflist=[]
                        remarks=''
                        hardcodedmn_jan=hardcodedmn_sep=hardcodedmn_dec=0
                        hardcodeddy_mon=hardcodeddy_wed=hardcodeddy_fri=0
                        frmtm=frmtd=frmty=frmtmm=frmtdd=frmtyy=0
                if beg!=-1:
                    cnt=cnt+1
            if '}' in l:
                if cnt==1:
                    if hardcodeddy_mon+hardcodeddy_wed+hardcodeddy_fri==3:
                        remarks+='Day Name Hardcoded/Translated as string\n'
                    if hardcodedmn_jan+hardcodedmn_sep+hardcodedmn_dec==3:
                        remarks+='Month Name Hardcoded/Translated as string\n'
                    if frmtm+frmtd+frmty>=2:
                        remarks+='Date Format Hardcoded- Case 1\n'
                    if frmtmm+frmtdd+frmtyy>=2:
                        remarks+='Date Format Hardcoded- Case 2\n'
                    end=i
                    prev_st=''
                    scope.append((beg,end,remarks,cflist))
                    beg=-1
                cnt-=1
                if cnt<0:
                    cnt=0
        file = open(fname, 'r',encoding=result['encoding'],errors="surrogateescape")
        file_content = file.read()
        file.close()
        
        try:
            for beg,end,rem,lst in scope:
                x=beg-1
                #print (lines_f[x],x)
                func=re.findall('[A-Za-z_][A-Za-z0-9_]*',lines_f[x])
                if func:
                    #print(func[0])
                    cursor.execute(sql_qry2,(fileid,filepath,typ,func[0].strip().split('(')[0],beg,end,file_content,rem))
                    db.commit()
                    cursor.execute(sql_qry3,(fileid,func[0].strip().split('(')[0],beg,end))
                    funcid=cursor.fetchone()
                    
                    for cfl in lst:
                        #print(func[0].strip().split('(')[0])
                        cursor.execute(sql_qry4,(fileid,funcid[0],typ,func[0].strip().split('(')[0],cfl))
                        db.commit()
            os.remove(fname)
        except:
            traceback.print_exc()
            print(f)

