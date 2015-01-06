# -*- coding : utf-8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
from db.mydb import MyDB
import time
from tornado.escape import json_encode
class HotInvester(Processor):
    
    def dowork(self):
        '''获取热门投资信息列表'''
        
        mydb = MyDB(self.conn)
        startindex = self.jsonbody['startindex']
        offset = self.jsonbody['offset']
        topicpubliclist = mydb.getPublicTopic(startindex,offset)
        topic_data = []
        for row in topicpubliclist:
#            onetopic = {}
#            onetopic['topicid'] = row['topicid']
#            onetopic['publisher_id']=row['publisher_id']
#            onetopic['title']=row['publisher_name']
#            onetopic['topic_type'] = row['topic_type']
#            onetopic['ptime'] = row['relation_key'] 
#            onetopic['content'] = row['content']
#            row['ctime']
            row['ptime'] = time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S")) - time.time()
            row['support_sum'] = mydb.getTopicSupportSum(row['topicid'])
            row['comment_sum'] = mydb.getTopicCommentSum(row['topicid'])
            row['tramsmit_sum'] = mydb.getTopicTramsmitSum(row['topicid'])
            topictype = row['topic_type']
            if topictype == 0:
                pass
            elif topictype ==1:
                closeoutinfo = mydb.getcloseoutTopicInfo(row['relation_key'])
                row['content'] = closeoutinfo
            elif topictype == 2:
                copyinfo = mydb.getcopyTopicInfo(row['relation_key'])
                row['content'] = copyinfo
            elif topictype == 3:
                commentinfo = mydb.getcommentInfo(row['relation_key'])
                row['content'] = commentinfo
            
            topic_data.append(row)
        self.handler.write(json_encode(topic_data))
        
        