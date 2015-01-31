# -*- coding:utf-8 -*-

'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
import time
from constants.constant import Topic_Constants
class TopicDetail(Processor):
    '''获取话题详情'''
    def dowork(self):
        
        topicid = int(self.handler.get_argument('topic_id',0))
        startindex = int(self.handler.get_argument('comment_startindex',0))
        topic_data = None
        if startindex ==0:
            topic_data = self.getTheTopicInfo(topicid)
            if not topic_data:
                self.response_fail("could't find the topic by topic Id!!!!")
        else:
            topic_data = self.getCommentLeve1(topicid, startindex)
        
        self.response_success(topic_data)
    
    def getTheTopicInfo(self,topicid):
        '''获取topic基本信息'''
     
        row_entity = self.mydb.getTopicInfo(topicid)
        if not row_entity:
            
            return None
        topic_obj = {}
        topic_obj['topicid'] = row_entity.topicid
        topic_obj['publisher_id'] = row_entity.publisher_id
        if row_entity.topic_type == 0 :  #文字  and 评论
            topic_obj['title'] = row_entity.publisher_name
            topic_obj['content'] = row_entity.content 
        elif row_entity.topic_type == 1: #平仓 
            closeoutinfo = self.mydb.getcloseoutTopicInfo(row_entity.relation_key)
            topic_obj['title'] = row_entity.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
            topic_obj['content'] = closeoutinfo
        topic_obj['ptime'] = int(time.time()) - int(time.mktime(time.strptime(row_entity['ctime'], "%Y-%m-%d %H:%M:%S"))) 
        topic_obj['support_sum'] = row_entity.support_sum
        topic_obj['comment_sum'] = row_entity.comment_sum
        topic_obj['tramsmit_sum'] = row_entity.tramsmit_sum
        topic_obj['topic_type'] = row_entity.topic_type
        commentlist = self.getCommentLeve1(topicid, 0)
        topic_obj['comment_list'] = commentlist
        return topic_obj
    
    def getCommentLeve1(self,topicid,startindex):
        comments_list = []
        level1_comments = self.mydb.getTopicOfCommentLevel1(topicid,startindex)
        for comment in level1_comments:
            comment['ptime'] = time.time() - time.mktime(time.strptime(comment['ctime'], "%Y-%m-%d %H:%M:%S"))
            discusslist = self.getCommentLeve2(comment.comment_id,0)
            comment['discuss_list'] = discusslist
            comments_list.append(comment)
        return comments_list
    
    def getCommentLeve2(self,byCommentid,startindex):
        discuss_list = []
        level2_comments = self.mydb.getTopicOfCommentLevel2(byCommentid,startindex)
        for discuss in level2_comments:
            discuss['ptime']= time.time() - time.mktime(time.strptime(discuss['ctime'], "%Y-%m-%d %H:%M:%S")) 
            discuss_list.append(discuss)
        return discuss_list
        