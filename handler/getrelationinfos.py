# -*- coding:utf-8 -*-
'''
Created on 2015-1-7

@author: fuwenbin
'''

from processor import Processor
from constants.constant import Topic_Constants
import time
from utils.filters import filterSensitive,getKeyVal
class GetRelationInfos(Processor):
    '''获取与某相关的投资信息'''
    def dowork(self):
        usercode = self.handler.get_argument('usercode',0)
        startindex = self.handler.get_argument('startindex',0)
        #获取相关的话题列表
                # 1.交易
                # 2.复制
                # 3 话题
        rows = self.mydb.getRelationInfo(usercode,startindex)
        all_data = {}
        topic_data = []
        mapKeyVal = {}
        for row in rows:
            row['ptime'] =  time.time()-time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S"))
            topicType = row['topic_type']
            if row['content']:
                row['content'] = filterSensitive(row['content'])
            if topicType == 0:
                row['title'] = row.publisher_name
                entities  = self.mydb.getContentKeys(row['topicid'])
                if entities:
                    mapKeyVal = dict(mapKeyVal,**getKeyVal(entities))
                pass
            elif topicType ==1: # closeout
                
                closeoutinfo = self.mydb.getcloseoutTopicInfo(row['relation_key'])
                row['title'] = row.publisher_name + " " + Topic_Constants.closeout_ch + " " + closeoutinfo.out_type
                row['relation'] = closeoutinfo
            elif topicType == 2: # copy 
                copyinfo = self.mydb.getcopyTopicInfo(row['relation_key'])
                row['title'] = row.publisher_name + "　" + Topic_Constants.copy_ing + " " + copyinfo.byname
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
 