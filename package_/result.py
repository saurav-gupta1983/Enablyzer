'''
Created on Mar 08, 2018

@author: shrbhatt
'''

import pymysql

db = pymysql.connect("Shrbhatt-wx-3","root","root","Enablyzer_Ppro" )

# prepare a cursor object using cursor() method
#`ResultID` bigint(20) NOT NULL AUTO_INCREMENT,
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS Result")
sql = """CREATE TABLE `Result` (
  `codefileid` bigint(20) DEFAULT NULL,
  `codedeclaredfuncid` bigint(20) DEFAULT NULL,
  `codepath` varchar(1000) DEFAULT NULL,
  `declared_func` varchar(1000),
  `Called_func` varchar(1000),
  `Remarks` LONGTEXT
)  ENGINE=InnoDB AUTO_INCREMENT=26311 DEFAULT CHARSET=utf8"""

cursor.execute(sql)
def dfs_recursive(vertex, path,level,fpath,sql):
    #path += [vertex]
    #print("ck3")
    if level>5:
        return
    if vertex=='main':
        return
    cursor.execute(sql,vertex)
    #print(vertex)
    graph = cursor.fetchall()
    #print(len(graph))
    for neighbor in graph:
        #print(neighbor[1],neighbor[2])
        if neighbor[2] not in path:
            #print(neighbor,path)
            level=level+1
            path.add(neighbor[2])
            fpath.add(neighbor[2])
            dfs_recursive(neighbor[2],path,level,fpath,sql)
            #path.remove(neighbor[1])
            level=level-1
            
def dfs_chk(vertex, path,level,fpath,sql):
    #path += [vertex]
    
    global res
    print(vertex,res,level)
    if res==1:
        return
    if level>3:
        return
    if vertex=='main':
        return
    if vertex in fpath:
        res=1
        return
        #print("Success")
    #cursor.execute(sql1,vertex)

    cursor.execute(sql,vertex)
    
    graph = cursor.fetchall()
    for neighbor in graph:
        #print(len(graph))
        if neighbor[2] not in path:
            #print(neighbor,path)
            level=level+1
            path.add(neighbor[2])
            dfs_chk(neighbor[2],path,level,fpath,sql)
            #path.remove(neighbor[1])
            level=level-1


sql_qry1 = "SELECT distinct codefileid,codedeclaredfuncid,declared_func FROM codeCalledfunc1 where called_func=(%s) "
sql_qry2 = "SELECT distinct * FROM codecalledfunc1 where called_func in (%s,%s,%s,%s,%s,%s,%s,%s) "
sql_qry3 = "SELECT distinct sourcefilepath FROM sourcefiles where sourceid= (%s)"
sql_qry4 = "SELECT distinct * FROM codecalledfunc1 where called_func= 'setlocale' "
sql_qry5 = "INSERT INTO Result(codefileid,codedeclaredfuncid,codepath,declared_func,called_func,remarks) VALUES(%s,%s,%s,%s,%s)"
sql_qry6 = "SELECT distinct codefileid,codedeclaredfuncid,declared_func,called_func FROM codecalledfunc1 where called_func in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
sql_qry7 = "SELECT distinct codefileid,codedeclaredfuncid,declared_func,called_func FROM codecalledfunc1 where called_func in (%s,%s,%s,%s) "
sql_qry8 = "SELECT distinct codefileid,codedeclaredfuncid,declared_func,called_func FROM codecalledfunc1 where called_func like 'GetDateFormat%' or called_func like 'GetTimeFormat%' or called_func ='imbue' or called_func='GetLocaleInfo'"
sql_qry9 = "SELECT distinct codefileid,codedeclaredfuncid,code_file,declared_func,remarks FROM codedeclaredfunc where remarks<> ''"

cursor.execute(sql_qry2,('strftime','ctime','asctime','localtime','GetLocalTime','local_time','DateString','TimeString','LongDateString','LongTimeString','ToFileTime'));
graph = cursor.fetchall()

#print("Calling Func     Called Func    Code Path    Comment")
ex_path=set()
path=set()
level=0

for gp in graph:
    cursor.execute(sql_qry3,gp[1]);
    gr = cursor.fetchone()
    if gp[5]=='strftime':
        cursor.execute(sql_qry4)
        dt=cursor.fetchall()
        if not dt:
            comment= "When strftime is used, setlocale() should be used , else will appear unlocalized"
    elif gp[5]=='ctime':
        comment= "Ctime is not a localised function"
    else:
        comment='GetLocalTime does not capture UTC timestamp, hence will appear correct only in LocalTimeZone.'
    #print(gp[5])
    cursor.execute (sql_qry5,(gp[1],gp[2],gr[0],gp[4],gp[5],comment)) 
    db.commit() 
 
cursor.execute(sql_qry6,('stat','last_write_time','FileTimeToSystemTime','GetSystemTime','get_system_time','GetFileTime','FindFirstFile','GetSystemTimeAsFileTime','Created','Modified','universal_time','ToFileTimeUtc''gmtime','time'));
graph = cursor.fetchall()
#print(len(graph))
for gp1 in graph:
    ex_path=set()
    path=set()
    path.add(gp1[2])
    ex_path.add(gp1[2])
    level=0
    #print(gp1)
    dfs_recursive(gp1[2], path, level, ex_path,sql_qry1)
    cursor.execute(sql_qry7,('FileTimetoLocalFileTime','utc_to_local','SystemTimeToTzSpecificLocalTime','ToLocalTime'));
    gr1 = cursor.fetchall()
    rs1=0
    for gp2 in gr1:
        #print(gp2)
        res=0
        path=set()
        path.add(gp2[2])
        fpath=ex_path
        level=0
        dfs_chk(gp2[2], path, level, fpath,sql_qry1)
        #print(g1[1])
        #print("res=",res)
        rs1=rs1|res;
        cursor.execute(sql_qry3,gp2[0]);
        gr2 = cursor.fetchone()
        '''comment= "If file metadata is stored in this format it appears correct only in Local TimeZone as does not save UTC timestamp for conversion"
        if gp2[3]=='FileTimetoLocalFileTime' or gp2[3]=='utc_to_local' or gp2[3]=='SystemTimeToTzSpecificLocalTime' or gp2[3]=='ToLocalTime':
            #print(gp2[0],gp2[1],gr2[0],gp2[2],gp2[3],comment)
            #print("chk1")
            cursor.execute (sql_qry5,(gp2[0],gp2[1],gr2[0],gp2[2],gp2[3],comment)) 
            db.commit() '''
    if rs1==0:
        #print(gp1[0])
        cursor.execute(sql_qry3,gp1[0]);
        gr5 = cursor.fetchone()
        comment= "UTC value - not localized"
        cursor.execute (sql_qry5,(gp1[0],gp1[1],gr5[0],gp1[2],gp1[3],comment)) 
        db.commit() 
        

cursor.execute(sql_qry7,('FileTimetoLocalFileTime','utc_to_local','SystemTimeToTzSpecificLocalTime','ToLocalTime'));
gr1 = cursor.fetchall()
for gp2 in gr1:
    path=set()
    path.add(gp2[2])
    ex_path=set()
    ex_path.add(gp2[2])
    level=0
    rs2=0
    dfs_recursive(gp2[2], path, level, ex_path,sql_qry1)
    cursor.execute(sql_qry8);
    gr3 = cursor.fetchall()
    for gp3 in gr3:
        #print(gp3)
        res=0
        path=set()
        path.add(gp3[2])
        fpath=ex_path
        level=0
        dfs_chk(gp3[2], path, level, fpath,sql_qry1)
        rs2=rs2|res
        #print(res)
    if rs2==0:
        cursor.execute(sql_qry3,gp2[0]);
        gr4 = cursor.fetchone()
        comment= "Standard Formatting not used"
        cursor.execute (sql_qry5,(gp2[0],gp2[1],gr4[0],gp2[2],gp2[3],comment)) 
        db.commit() 
cursor.execute(sql_qry9);
gr = cursor.fetchall()
for gp in gr:
    cursor.execute (sql_qry5,(gp[0],gp[1],gp[2],gp[3],"",gp[4])) 
    db.commit() 
  
db.close()  
        