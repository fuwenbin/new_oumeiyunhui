#-*- coding:utf-8 -*-
'''
Created on 2015-1-30

@author: fuwenbin
'''

from processor import Processor
class FollowList(Processor):
    def dowork(self):
        startindex = self.handler.get_argument('startIndex',0)
        offset = self.handler.get_argument('offset',10)
        usercode = self.handler.get_argument('userCode',0)
        type = self.handler.get_argument('type',0)
        
        if not type:
            entities = self.mydb.getFansList(startindex, offset, usercode)
            self.response_success(entities)
        else:
            entities = self.mydb.getbFansList(startindex, offset, usercode)
            self.response_success(entities)