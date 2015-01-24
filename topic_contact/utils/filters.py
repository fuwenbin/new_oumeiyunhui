# -*- coding:utf-8 -*-
'''
Created on 2015-1-24

@author: fuwenbin
'''
import re

specialwords = ''',<.>/?;:'\"[{]}\\|`~!@#$%^&*()-=+ \r\n\t'''   


def filterSqlSpecialWord(words):
    regex = re.compile('''[,<.>/?;:'\"[{]}\\|`~!@#$%^&*()-=+ \r\n\t]''')
    
    words = regex.sub(lambda m: '['+strB2Q(m.group(0))+']',words)
    print words
    return words
    
def strB2Q(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring




filterSqlSpecialWord("""asdfadsfasdfasdf<>>>>>>>>>>>>>""")
#print strB2Q("""<>>>>>>""")