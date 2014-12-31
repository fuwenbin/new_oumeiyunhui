'''
Created on 2014-12-31

@author: fuwenbin
'''

import redis
import threading

stop_server = False
class RedisReading(threading.Thread):
    '''connect redis to get data !!!'''
    def __init__(self,host,port,db,pwd,conn):
        self.redis = redis.Redis(host=host,port = port,db=db,password=pwd)
        
    def saveUserToLocal(self):
        pass
    
    def saveTracdesToLocal(self):
        pass
    
    def saveCopyTolocal(self):
        pass
        
    def run(self):
        
        while True:
            
            
            
    
    
    
    