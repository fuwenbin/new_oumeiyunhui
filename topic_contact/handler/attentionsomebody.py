# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor

class AttentionSomeBody(Processor):
    """关注某人"""
    def dowork(self):
        usercode = self.handler.get_argument('usercode',0)
        byattentionid = self.handler.get_argument('by_attention_id')
        statecode = self.mydb.attentionOne(usercode, byattentionid)
        if statecode ==1:
            self.response_fail("重复关注")
        else:
            self.response_success()
        
