'''
Created on Dec 8, 2017

@author: shrbhatt
'''
import pymysql
import os
#from os.path import dirname
# Open database connection
db = pymysql.connect("shrbhatt-wx-3","root","root","Enablyzer_Ppro" )
# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS SourceFiles")

# Create table as per requirement
sql = """CREATE TABLE `Sourcefiles` (
  `SourceID` bigint(20) NOT NULL AUTO_INCREMENT,
  `ProductID` bigint(50) DEFAULT NULL,
  `SourceFilePath` varchar(255) NOT NULL,
  `UpdatedBy` varchar(50) DEFAULT NULL,
  `UpdatedOn` datetime DEFAULT NULL,
  `AddedBy` varchar(50) DEFAULT NULL,
  `AddedOn` datetime DEFAULT NULL,
  `Type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SourceID`),
  UNIQUE KEY `UX_SourceFIles` (`ProductID`,`SourceFilePath`),
  KEY `IX_ProductID` (`ProductID`),
  KEY `IX_SourceFiles` (`SourceFilePath`)
) ENGINE=InnoDB AUTO_INCREMENT=126309 DEFAULT CHARSET=utf8"""

cursor.execute (sql)

sql="""INSERT INTO SourceFiles(SourceFilePath,Type) VALUES (%s,%s)"""
folder="//parulgup-Wx-1/PremierePro"

#parent_folder = dirname(dirname(folder))
files = [os.path.join(r, f) for r,d,fn in os.walk(folder) for f in fn if f.endswith('.h') or f.endswith('.hpp') or f.endswith('.hh') or f.endswith('.c') or f.endswith('.cpp') or f.endswith('.cc')]
print(len(files))
typ=''
for f in files:
    if f.endswith('.h') or f.endswith('.hh') or f.endswith('.hpp'):
        typ='UserDefined_Header'
    else:
        typ='Code'
    #path=f[f.index(parent_folder) + len(parent_folder):]
    #name=os.path.basename(folder)
    #print(f)
    cursor.execute (sql,(f,typ) )
    db.commit();


# disconnect from server
db.close()