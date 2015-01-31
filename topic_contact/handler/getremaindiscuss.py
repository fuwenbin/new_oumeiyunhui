#-*- coding:utf8 -*-
'''
Created on 2015-1-31

@author: fuwenbin
'''
from processor import Processor
import time
class GetRemainDiscuss(Processor):
    
    def dowork(self):
        byCommentId = self.handler.get_argument('by_comment_id',0)
        startId = self.handler.get_argument('start_id',0)
        if not byCommentId:
            self.response_fail("your argument:by_comment_id war not right!!!")
            return 
        discuss_list = []
        level2_comments = self.mydb.getTopicOfCommentLevel2(byCommentId,startId)
        for discuss in level2_comments:
            discuss['ptime']= time.time() - time.mktime(time.strptime(discuss['ctime'], "%Y-%m-%d %H:%M:%S")) 
            discuss_list.append(discuss)
        self.response_success(discuss_list)
        