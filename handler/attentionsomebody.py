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
        action = int(self.handler.get_argument('action'))
        if action ==1:
            statecode = self.mydb.attentionOne(usercode, byattentionid)
            if statecode:
                self.response_fail("重复关注")
                return
        else:
            statecode = self.mydb.cancleAttention(usercode, byattentionid)
            if statecode:
                self.response_fail("取消失败")
                return
        self.response_success()
        
