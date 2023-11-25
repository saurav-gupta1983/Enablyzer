'''
Created on Mar 8, 2018

@author: shrbhatt
'''
import pymysql

# Open database connection

db = pymysql.connect("shrbhatt-wx-3","root","root" )
db.cursor().execute('create schema if not exists Enablyzer_Ppro character set UTF8 collate utf8_general_ci')
#character set UTF8 collate utf8_general_ci;
# prepare a cursor object using cursor() method
db.commit()
db.close()


import xyz.sourcefiles
import xyz.codefiles
import xyz.calledFunc
import xyz.declaredFunc
import xyz.result
