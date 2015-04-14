# -*- coding:utf-8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
from processor import Processor
import time
from utils.filters import filterSensitive,getKeyVal
class HotInvester(Processor):
    
    def dowork(self):
        '''获取热门投资列表'''
        
        startindex = self.handler.get_argument('startindex',0)
        topicpubliclist = self.mydb.getPublicTopic(int(startindex))
        all_data = {}
        topic_data = []
        mapKeyVal = {}
        for row in topicpubliclist:
            row['ptime'] = int(time.time()) - int(time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S")))
            topicType = row['topic_type']
            
            row['tramsmit_list'] = self.mydb.getTopicTramsmitUlist(row['topicid'])
            
            if row['content']:
                row['content'] = filterSensitive(row['content'])
            if topicType == 0:
#                row['title'] = row.publisher_name
                entities  = self.mydb.getContentKeys(row['topicid'])
                if entities:
                    mapKeyVal = dict(mapKeyVal,**getKeyVal(entities))
            elif topicType ==1: # closeout
                
                closeoutinfo = self.mydb.getcloseoutTopicInfo(row['relation_key'])
#                row['title'] = row.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
                row['relation'] = closeoutinfo
            elif topicType == 2: # copy 
                copyinfo = self.mydb.getcopyTopicInfo(row['relation_key'])
#                row['title'] = row.publisher_name + "　" + Topic_Constants.copy_ing + " " + copyinfo.byname
                copyinfo['be_follow_sum'] = row.content
                row['relation'] = copyinfo
            elif topicType == 3:  #tramsmit 
                tramsmit_id = row.tramsmit_id
                byTramsmit_topicinfo = self.mydb.getTopicInfo(tramsmit_id)   
                byTramsmit_topicinfo['ptime'] = time.time()-time.mktime(time.strptime(byTramsmit_topicinfo['ctime'], "%Y-%m-%d %H:%M:%S"))
                row['relation'] = byTramsmit_topicinfo
            topic_data.append(row)
            all_data['list'] = topic_data
            all_data['mapKeyVal'] = mapKeyVal
        self.response_success(all_data)
        
        