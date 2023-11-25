'''
Created on 20 mars 2018

@author: shrbhatt
'''
import os
import re
import pymysql
import chardet
import traceback

#cf1=re.findall('[(A-Z)\(a-z)\\_][(A-Z)\(a-z)\\_\(0-9)]*',"WcharToUTF16(outputStr.c_str())")
func=re.findall('[A-Za-z_][A-Za-z0-9_]*\s=\sfunction\s*\(','_G.import = function( ... )')
print(func)
       