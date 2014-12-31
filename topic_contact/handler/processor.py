'''
Created on 2014-12-31

@author: fuwenbin
'''
from db.mydb import MyDB

class Processor():
    ''' this is handler's super class'''
    def __init__(self,requesthandler):
        self.handler = requesthandler
        
        self.redis = requesthandler.applicatoin.redis
        
        self.mydb = MyDB(self.application.conn)
        
    def testPost(self):
        
        pass