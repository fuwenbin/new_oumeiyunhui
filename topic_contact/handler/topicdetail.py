# -*- coding:utf-8 -*-

'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
from db.mydb import MyDB
from tornado.escape import json_encode
class TopicDetail(Processor):
    '''获取话题详情'''
    def dowork(self):
        
        mydb = MyDB(self.conn)
        topicid = self.jsonbody['topic_id']
        
        row_entity = mydb.getTopicInfo(topicid)
        level0_comments = mydb.getTopicOfCommentLevel1(row_entity.topic_id)
        topic_obj = {}
        topic_obj['topicid']
        topic_obj['publisher_id']
        topic_obj['title']
        topic_obj['ptime']
        topic_obj['support_sum']
        topic_obj['comment_sum']
        topic_obj['topic_type']
        topic_obj['content']
        
        comments_list = []
        for comment in level0_comments:
            comment_obj = {}
            comment_obj['topicid']
            comment_obj['publisher_name']
            comment_obj['publisher_icon']
            comment_obj['publisher_icon']
            comment_obj['support_sum']
            comment_obj['title']
            comment_obj['ptime']
            
            
            discuss_list = []
            level1_comments = mydb.getTopicOfCommentLevel2(comment.topic_id, comment.by_comment_id)
            for discuss in level1_comments:
                discuss_obj = {}
                discuss_obj['publisher_id']
                discuss_obj['publisher_name']
                discuss_obj['publisher_icon']
                discuss_obj['content']
                discuss_obj['ptime']
                discuss_obj['support_sum']
                discuss_obj['discuss_sum']
                
                discuss_list.append(discuss_obj)
            comment_obj['discuss_list']
            comments_list.append(comment_obj)
            
        
        topic_obj['comment_list'] = comments_list
        
        self.handler.write(json_encode(topic_obj))