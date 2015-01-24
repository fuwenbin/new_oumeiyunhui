# -*- coding:utf8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''
from utils.errors import Errors
from processor import Processor
class Support(Processor):
    """话题或者评论点赞"""
    def dowork(self):
        type_d = int(self.handler.get_argument('type',1000))
        usercode = self.handler.get_argument('usercode',0)
        topicid = self.handler.get_argument('topicid',0)
        try:
            if type_d ==0:
                self.mydb.supportTopic(topicid, usercode)
            elif type_d == 1:
                self.mydb.supportComment(topicid,usercode)
        except:
#            Errors.TraceErrorHandler(self)
            self.response_fail(u"support too much!!")
            return
        self.response_success()