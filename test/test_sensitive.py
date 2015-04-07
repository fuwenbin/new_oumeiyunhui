#-*- coding:utf-8 -*-
'''
Created on 2015-3-3

@author: fuwenbin
'''
from constants.sensitive import sensitive_words
import re

def test():
    be_words = r"的啊发地方   jghgugjokoujuin爱的上看风景爱快乐的减肥垃圾啦发了看见  押题 地方噶地方啊   预测答案"
    ad = u'的|u|押题'
    partten = re.compile(sensitive_words)
    
    n_words = partten.sub(r'*',be_words)
    print n_words
    
    
test()