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
        type_d = self.handler.get_argument('type',1000)
        usercode = self.handler.get_argument('usercode',0)
        content = self.handler.get_argument('content',"")
        topicid = self.handler.get_argument('topicid',0)
        print "comment arguments is : %s , %s, %s ,%s"%(type_d,usercode,content,topicid)
    
        insertid = 0
        obj = {}
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
        if int(type_d) ==0:
            topicinfo = self.mydb.getTopicInfo(topicid)
            if not topicinfo:
                self.response_fail("cant find the topic by topicid")
                return
            insertid=self.mydb.commentTopic(usercode, topicid, 0, content,ctime)
            if insertid:
                obj['comment_sum'] = 0
                obj['comment_publisherid'] = usercode
                obj['by_comment_id'] = 0
                obj['ptime'] = 1
                obj['comment_id'] = insertid
                obj['content'] = content
                obj['support_sum'] =0
                obj['discuss_list']=[]
                obj['by_topicid']= topicid
                obj['publisher_name']=self.mydb.getusername(usercode)
        elif int(type_d) ==1:
            bycommentid = topicid
            topicid = self.mydb.getTopicIdByCommentId(bycommentid)
            if not topicid:
                self.response_fail("cant find the comment by topicid")
                return
            insertid=self.mydb.commentTopic(usercode, topicid, bycommentid, content,ctime)
            if insertid:
                obj['comment_sum'] = 0
                obj['comment_publisherid'] = usercode
                obj['by_comment_id'] = bycommentid
                obj['ptime'] = 1
                obj['comment_id'] = insertid
                obj['content'] = content
                obj['support_sum'] =0
                obj['by_topicid']= topicid
                obj['publisher_name']=self.mydb.getusername(usercode)
        relist = re.findall(r'@\S ',content)  
        if len(relist)>0:
            for reobj in relist:
                atstr = re.sub(r'@',reobj)
                self.mydb.mapconentkey(atstr, 1, insertid, ctime)
                
        
        self.response_success(obj)
        