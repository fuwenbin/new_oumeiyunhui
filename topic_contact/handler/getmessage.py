#-*- coding:utf8 -*-
'''
Created on 2015-2-7

@author: fuwenbin
'''
from handler.processor import Processor
class GetMessage(Processor):
    def dowork(self):
        
        usercode = self.handler.get_argument('usercode',0)
        startindex = self.handler.get_argument('startindex',"")
        offset = int(self.handler.get_argument('offset',10))
        
        sys_msgs,user_msgs = self.mydb.getMessage(usercode, startindex, offset)
        data = {}
        data['sys'] = sys_msgs
        data['user'] = user_msgs
        self.response_success(data)