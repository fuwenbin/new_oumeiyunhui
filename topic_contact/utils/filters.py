# -*- coding:utf-8 -*-
'''
Created on 2015-1-24

@author: fuwenbin
'''
import re

specialSqlWords = '''[\,\<\.\>\/\?;:\'\"\[\{\]\}\\\\\|\`\~\!@#\$\%\^\&\*\(\)\-\=\+\000\r\n\t]'''   


def filterSqlSpecialWord(words):
    regex = re.compile(specialSqlWords)
    
    words = regex.sub(strB2Q,words)
    print words
    return words
    
def strB2Q(matched):
    ustring = matched.group(0)
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring




#filterSqlSpecialWord("""asdfadsfasdfasd , , , [ [  ]]]  {}  ! #@ #　%  f<>>>>>>>>>>>>>""")
#print strB2Q("""<>>>>>>""")