# -*- coding:utf8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''
from processor import Processor
from utils.errors import Errors
class GetAttentionAndFansInfo(Processor):
    '''获取关注和粉丝数量'''
    
    def dowork(self):
        try:
            usercode = self.handler.get_argument('usercode',0)
            current_code = self.handler.get_cookie('userCode',0)
        except:
            Errors.TraceErrorHandler(self)
            self.response_fail("arguments errors")
        data = self.mydb.getfansInfos(usercode)
        isfans = self.mydb.isFan(current_code,usercode)
        data['is_by_attention'] = isfans
        self.response_success(data)