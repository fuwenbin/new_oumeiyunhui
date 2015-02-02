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
        fansinfo = self.mydb.getfansInfos(usercode)
        entities = None
        if type:
            entities = self.mydb.getFansList(startindex, offset, usercode)
        else:
            entities = self.mydb.getbFansList(startindex, offset, usercode)
        json_struct = {}
        json_struct['list'] = entities
        json_struct['fan_info']=fansinfo
        self.response_success(json_struct)
        
    