# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor

class Comment(Processor):
    """评论话题或者  评论"""
    def dowork(self):
        type_d = self.jsonbody['type']
        usercode = self.jsonbody['usercode']
        content = self.jsonbody['content']
        topicid = self.jsonbody['topicid']
        if type_d ==0:
            self.mydb.commentTopic(usercode, topicid, 0, content)
        elif type_d ==1:
            bycommentid = topicid
            topicid = self.mydb.getTopicIdByCommentId(bycommentid)
            self.mydb.commentTopic(usercode, topicid, bycommentid, content)
        self.response_success()
        