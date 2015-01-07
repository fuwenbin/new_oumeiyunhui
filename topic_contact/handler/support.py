# -*- coding:utf8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor
class Support(Processor):
    """话题或者评论点赞"""
    def dowork(self):
        type_d = self.jsonbody['type']
        usercode = self.jsonbody['usercode']
        topicid = self.jsonbody['topicid']
        if type_d ==0:
            self.mydb.supportTopic(topicid, usercode)
        elif type_d == 1:
            self.mydb.supportComment(topicid,usercode)