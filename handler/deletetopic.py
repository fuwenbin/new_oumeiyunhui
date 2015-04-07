# -*- coding:utf8 -*-
'''
Created on 2015-1-8

@author: fuwenbin
'''

from processor import Processor

class DeleteTopic(Processor):
    
    def dowork(self):
        usercode = self.handler.get_argument('usercode',0)
        typecode = int(self.handler.get_argument('type',0))
        topicid = self.handler.get_argument('topicid',0)
        rowcount = 0
        if typecode == 0:
            rowcount = self.mydb.deletetopic(usercode,topicid)
        elif typecode ==1:
            rowcount = self.mydb.deletecomment(usercode,topicid)
            
        if rowcount==1:
            self.response_success()
        else:
            self.response_fail("delete fail,because can not find object or you have no permission!!")