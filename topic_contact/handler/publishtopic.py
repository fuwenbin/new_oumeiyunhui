# -*-coding:utf-8 -*-

'''
Created on 2015-1-6

@author: fuwenbin
'''

from processor import Processor
class PublishTopic(Processor):
    '''发表话题'''
    def dowork(self):
        publisher_id = self.jsonbody['publisher_id']
        content = self.jsonbody['content']
        data = {}
        data['publisherid'] = publisher_id
        data['content'] = content
        data['topictype'] = 0
        data['relationkey'] = 0
        data['publishername'] = self.mydb.getusername(publisher_id)
        data['ispublic']  = 0
        self.mydb.publishtopic(data)
        