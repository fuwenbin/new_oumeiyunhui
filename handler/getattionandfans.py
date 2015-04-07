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
        usercode = 0
        current_code = ''
        try:
            usercode = self.handler.get_argument('usercode',0)
            current_code = self.handler.get_argument('personal_usercode','')
        except:
            Errors.TraceErrorHandler(self)
            self.response_fail("arguments errors")
        data = self.mydb.getfansInfos(usercode)
        isfans = self.mydb.isFan(current_code,usercode)
        data['is_by_attention'] = isfans
        sys_unvisited_sum,user_unvisited_sum = self.mydb.getUnVisitedInfo(usercode)
        self.handler.set_cookie('sys_unvisited_sum',str(sys_unvisited_sum))
        self.handler.set_cookie('user_unvisited_sum',str(user_unvisited_sum))
        self.response_success(data)