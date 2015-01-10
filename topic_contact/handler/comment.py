# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor
import re
import time
class Comment(Processor):
    """评论话题或者  评论"""
    def dowork(self):
        type_d = self.jsonbody['type']
        usercode = self.jsonbody['usercode']
        content = self.jsonbody['content']
        topicid = self.jsonbody['topicid']
        insertid = 0
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
        if type_d ==0:
            topicinfo = self.mydb.getTopicInfo(topicid)
            if not topicinfo:
                self.response_fail("cant find the topic by topicid")
                return
            insertid=self.mydb.commentTopic(usercode, topicid, 0, content,ctime)
        elif type_d ==1:
            bycommentid = topicid
            topicid = self.mydb.getTopicIdByCommentId(bycommentid)
            if not topicid:
                self.response_fail("cant find the topic by topicid")
                return
            insertid=self.mydb.commentTopic(usercode, topicid, bycommentid, content,ctime)
        relist = re.findall(r'@\S ',content)  
        if len(relist)>0:
            for reobj in relist:
                atstr = re.sub(r'@',reobj)
                self.mydb.mapconentkey(atstr, 1, insertid, ctime)
        self.response_success()
        