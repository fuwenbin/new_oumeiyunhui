# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor
from constants.constant import Topic_Constants
import time
class GetRelationInfos(Processor):
    '''获取与自己相关的投资信息'''
    def dowork(self):
        usercode = self.handler.get_argument('usercode',0)
        startindex = self.handler.get_argument('startindex',0)
        offset = self.handler.get_argument('offset',0)
        rows = self.mydb.getRelationInfo(usercode,startindex,offset)
        topic_data = []
        for row in rows:
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
#            elif topictype == 3:  # discuss 
#                commentinfo = self.mydb.getcommentInfo(row['relation_key'])
#                row['content'] = commentinfo
            topic_data.append(row)
        self.response_success(topic_data)