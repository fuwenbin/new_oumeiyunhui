# -*- coding:utf-8 -*-
'''
Created on 2015-1-24

@author: fuwenbin
'''
import re
from constants.sensitive import sensitive_words

def filterSqlSpecialWord(words):
    specialSqlWords = '''[\,\<\.\>\/\?;:\'\"\[\{\]\}\\\\\|\`\~\!@#\$\%\^\&\*\(\)\-\=\+\000\r\n\t]'''   
    regex = re.compile(specialSqlWords)
    
    words = regex.sub(strB2Q,words)
    return words

def filterSensitive(content):
    partten = re.compile(sensitive_words)
    return partten.sub(u'*',content)

def getKeyVal(rows):
    
    atKeyVal = {}
    for dx in rows:
        atKeyVal[dx.atstr] = dx.relation_code
    return atKeyVal

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

def filterplaceholder(content):
    '''对% 符号进行过滤处理   主要在sql中防止参数中有%符号'''
    byrep = re.sub(r'%', '%%', content)

    return byrep
# filterplaceholder('')
#filterSqlSpecialWord("""asdfadsfasdfasd , , , [ [  ]]]  {}  ! #@ #　%  f<>>>>>>>>>>>>>""")
#print strB2Q("""<>>>>>>""")