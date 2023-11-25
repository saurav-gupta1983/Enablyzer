'''
Created on Dec 15, 2017

@author: shrbhatt
'''
import traceback
import re
import pymysql
import chardet

db = pymysql.connect("shrbhatt-wx-3","root","root","Enablyzer_Ppro" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
#data = cursor.fetchone()
cursor.execute("DROP TABLE IF EXISTS CodeFiles")

# Create table as per requirement
sql = """CREATE TABLE `codefiles` (
  `CodeFileID` bigint(20) NOT NULL AUTO_INCREMENT,
  `SourceFileID` bigint(20) DEFAULT NULL,
  `IncludeFileID` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`CodeFileID`),
  KEY `FK_SourceFiles` (`SourceFileID`),
  KEY `FK_HeaderFiles` (`IncludeFileID`) USING BTREE,
  CONSTRAINT `FK_CodeFiles` FOREIGN KEY (`SourceFileID`) REFERENCES `Sourcefiles` (`SourceID`),
  CONSTRAINT `FK_IncludeFiles` FOREIGN KEY (`IncludeFileID`) REFERENCES `Sourcefiles` (`SourceID`)
) ENGINE=InnoDB AUTO_INCREMENT=371530 DEFAULT CHARSET=utf8"""

cursor.execute (sql)

sql= """SELECT SourceID,SourceFilePath from SourceFiles where type='Code' or type='UserDefined_Header'"""
cursor.execute (sql)

files= cursor.fetchall()

sql="""INSERT INTO CodeFiles(SourceFileID,IncludeFileID) VALUES (%s,%s)"""
sql1="""INSERT INTO SourceFiles(SourceFilePath,type) VALUES (%s,%s)"""
for f in files:
    try:
        rawdata=open(f[1],"rb").read()
        result=chardet.detect(rawdata)
        with open(f[1],encoding=result['encoding'],errors="surrogateescape") as fin:
            lines=fin.readlines()
        for l in lines:
            l=l.strip()
            regexp = re.compile('#\s*include(.*)')
            if regexp.search(l):
                hf=regexp.search(l).group(1).strip().strip('"').lstrip('<').rstrip('>').lstrip('.').lstrip('/').lstrip('\\').split('.')[0]
                print(hf)
                if '.hpp' in l:
                    hf+='.hpp'
                elif '.hh' in l:
                    hf+='.hh'
                elif '.h' in l:
                    hf+='.h'
                hf=hf.strip().strip('"').strip()
                sql2="""SELECT SourceId from SourceFiles where (type='System_Header' or type='UserDefined_Header') and SourceFilePath like %s"""
                cursor.execute(sql2,'%\\\\'+hf)
                data=cursor.fetchall()
                if not data:
                    print(hf)
                    cursor.execute(sql1,(hf,'System_Header'))
                    db.commit();
                cursor.execute(sql2,'%\\\\'+hf)
                data=cursor.fetchall()
                for d in data:
                    cursor.execute(sql,(f[0],d[0]))
                    db.commit();
        fin.close()
    except:
        traceback.print_exc()
# disconnect from server
db.close()
