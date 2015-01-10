# -*- coding:utf8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''
from processor import Processor
class GetAttentionAndFansInfo(Processor):
    '''获取关注和粉丝数量'''
    
    def dowork(self):
        usercode = self.jsonbody['usercode']
        data = self.mydb.getfansInfos(usercode)
        self.response_data(data)