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
        
        topicid = self.handler.get_argument('topic_id',0)
        row_entity = self.mydb.getTopicInfo(topicid)
        if not row_entity:
            self.response_fail("could't find the topic by topic Id!!!!")
            return
        topic_obj = {}
        topic_obj['topicid'] = row_entity.topicid
        topic_obj['publisher_id'] = row_entity.publisher_id
        if row_entity.topic_type == 0 :  #文字  and 评论
            topic_obj['title'] = row_entity.publisher_name
            content = {}
            content['text'] = row_entity.content
            topic_obj['content'] = content 
        elif row_entity.topic_type == 1: #平仓 
            closeoutinfo = self.mydb.getcloseoutTopicInfo(row_entity.relation_key)
            topic_obj['title'] = row_entity.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
            topic_obj['content'] = closeoutinfo
        topic_obj['ptime'] = int(time.time()) - int(time.mktime(time.strptime(row_entity['ctime'], "%Y-%m-%d %H:%M:%S"))) 
        topic_obj['support_sum'] = row_entity.support_sum
        topic_obj['comment_sum'] = row_entity.comment_sum
        topic_obj['tramsmit_sum'] = row_entity.tramsmit_sum
        topic_obj['topic_type'] = row_entity.topic_type
        comments_list = []
        level1_comments = self.mydb.getTopicOfCommentLevel1(row_entity.topicid)
        for comment in level1_comments:
            comment['ptime'] = time.mktime(time.strptime(comment['ctime'], "%Y-%m-%d %H:%M:%S")) - time.time()
            discuss_list = []
            level2_comments = self.mydb.getTopicOfCommentLevel2(comment.topic_id,comment.by_comment_id)
            for discuss in level2_comments:
                discuss['ptime']= time.mktime(time.strptime(discuss['ctime'], "%Y-%m-%d %H:%M:%S")) - time.time()
                discuss_list.append(discuss)
            comments_list.append(comment)
        topic_obj['comment_list'] = comments_list
        self.response_success(topic_obj)