'''
Created on 2014-12-31

@author: fuwenbin
'''
from db.mydb import MyDB
from tornado.escape import json_decode
class Processor():
    ''' this is handler's super class'''
    def __init__(self,requesthandler):
        self.handler = requesthandler
        if requesthandler.request.body is not '':
            jsonbody = json_decode(requesthandler.request.body)
        self.redis = requesthandler.applicatoin.redis
        self.jsonbody= jsonbody
        self.mydb = MyDB(self.application.conn)
        
    def testPost(self):
        
        pass