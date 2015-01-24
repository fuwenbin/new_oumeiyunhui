# -*- coding:utf-8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
import time
from constants.constant import Topic_Constants
class HotInvester(Processor):
    
    def dowork(self):
        '''获取热门投资列表'''
        
        startindex = self.handler.get_argument('startindex',0)
        offset = self.handler.get_argument('offset',0)
        topicpubliclist = self.mydb.getPublicTopic(int(startindex),int(offset))
        topic_data = []
        for row in topicpubliclist:
            row['ptime'] = int(time.time()) - int(time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S")))
            topictype = row['topic_type']
            if topictype == 0:
                row['title'] = row.publisher_name
                pass
            elif topictype ==1: # closeout
                
                closeoutinfo = self.mydb.getcloseoutTopicInfo(row['relation_key'])
#                row['title'] = row.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
                row['content'] = closeoutinfo
            elif topictype == 2: # copy 
                copyinfo = self.mydb.getcopyTopicInfo(row['relation_key'])
#                row['title'] = row.publisher_name + "　" + Topic_Constants.copy_ing + " " + copyinfo.byname
                copyinfo['be_follow_sum'] = row.content
                row['content'] = copyinfo
            topic_data.append(row)
        self.response_success(topic_data)
        
        