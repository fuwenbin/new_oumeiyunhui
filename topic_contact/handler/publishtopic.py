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
        publisher_id = self.jsonbody['publisher_id']
        content = self.jsonbody['content']
        bytramsmitid = self.jsonbody['bytramsmitid']
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
        re_list = re.findall(r'@\S ',content)
        if len(re_list)>0:
            for reobj in re_list:
                atstr = reobj.sub(r"@","")
                self.mydb.mapconentkey(atstr, 0, insertid, ctime)
        
        if bytramsmitid is not 0:
            self.mydb.maptramsmit(bytramsmitid, publisher_id)
        self.response_success()
