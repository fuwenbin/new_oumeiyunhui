# -*-coding:utf-8 -*-

'''
Created on 2015-1-6

@author: fuwenbin
'''

from processor import Processor
import re
import time
class PublishTopic(Processor):
    '''发表话题'''
    def dowork(self):
        print "doworking start"
        publisher_id = self.handler.get_argument('publisher_id',0)
        content = self.handler.get_argument('content',"")
        bytramsmitid = int(self.handler.get_argument('bytramsmitid',0))
        
        data = {}
        data['publisher_id'] = publisher_id
        if bytramsmitid:
            pass
        data['content'] = content
        data['topic_type'] = 0
        data['relation_key'] = 0
        data['publisher_name'] = self.mydb.getusername(publisher_id)
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        data['ctime'] = ctime
        data['tramsmit_id'] = bytramsmitid
        data['ispublic'] = 0
        insertid = self.mydb.publishtopic(data)
        data['ptime'] = 1
        data['topicid'] = insertid
        data['comment_sum']=0
        data['support_sum']=0
        data['tramsmit_sum']=0
        re_list = re.findall(r'@\S+',content)
        if len(re_list)>0:
            for reobj in re_list:
                atstr = reobj.replace('@','')
                userCode = self.mydb.getUserByName(atstr)
                self.mydb.mapconentkey(reobj , 0, insertid, ctime,userCode) 
                   
        re_list = re.findall('\$\\S+',content)
        if len(re_list)>0:
            for reobj in re_list:
                self.mydb.mapconentkey(reobj, 0, insertid, ctime)   
        self.response_success(data)
