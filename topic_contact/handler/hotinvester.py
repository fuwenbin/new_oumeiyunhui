# -*- coding:utf-8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
import time
from tornado.escape import json_encode
from constants.constant import Topic_Constants
class HotInvester(Processor):
    
    def dowork(self):
        '''获取热门投资列表'''
        
        startindex = self.jsonbody['startindex']
        offset = self.jsonbody['offset']
        topicpubliclist = self.mydb.getPublicTopic(startindex,offset)
        topic_data = []
        for row in topicpubliclist:
            row['ptime'] = time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S")) - time.time()
            topictype = row['topic_type']
            if topictype == 0:
                row['title'] = row.publisher_name
                pass
            elif topictype ==1: # closeout
                
                closeoutinfo = self.mydb.getcloseoutTopicInfo(row['relation_key'])
                row['title'] = row.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
                row['content'] = closeoutinfo
            elif topictype == 2: # copy 
                copyinfo = self.mydb.getcopyTopicInfo(row['relation_key'])
                row['title'] = row.publisher_name + "　" + Topic_Constants.copy_ing + " " + copyinfo.byname
                copyinfo['be_follow_sum'] = row.content
                row['content'] = copyinfo
            elif topictype == 3:  # discuss 
                commentinfo = self.mydb.getcommentInfo(row['relation_key'])
                row['content'] = commentinfo
            topic_data.append(row)
        self.response_data(json_encode(topic_data))
        
        