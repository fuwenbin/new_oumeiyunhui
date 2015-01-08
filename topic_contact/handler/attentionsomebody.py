# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor

class AttentionSomeBody(Processor):
    """关注某人"""
    def dowork(self):
        usercode = self.jsonbody['usercode']
        byattentionid = self.jsonbody['by_attention_id']
        self.mydb.attentionOne(usercode, byattentionid)
        self.response_success()
        
