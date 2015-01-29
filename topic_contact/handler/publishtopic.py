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
        data['publisherid'] = publisher_id
        data['content'] = content
        data['topictype'] = 0
        data['relationkey'] = 0
        data['publishername'] = self.mydb.getusername(publisher_id)
        data['ispublic']  = 0
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        data['ctime'] = ctime
        insertid = self.mydb.publishtopic(data)
        data['comment_id']
        re_list = re.findall(r'@\S ',content)
        if len(re_list)>0:
            for reobj in re_list:
                atstr = reobj.sub(r"@","")
                self.mydb.mapconentkey(atstr, 0, insertid, ctime)
        
        if bytramsmitid is not 0:
            try:
                self.mydb.maptramsmit(bytramsmitid, publisher_id)
            except:
                self.response_fail("重复转发!!")
                return
        
        
        
        self.response_success()
