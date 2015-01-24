# -*- coding:utf8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''
from processor import Processor
class GetAttentionAndFansInfo(Processor):
    '''获取关注和粉丝数量'''
    
    def dowork(self):
        usercode = self.handler.get_argument('usercode',0)
        data = self.mydb.getfansInfos(usercode)
        self.response_success(data)