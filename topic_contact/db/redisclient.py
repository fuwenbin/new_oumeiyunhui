'''
Created on 2014-12-31

@author: fuwenbin
'''

import redis
import threading
import time

stop_server = False
class RedisReading(threading.Thread):
    '''connect redis to get data !!!'''
    def __init__(self,host,port,db,pwd):
#        pool = redis.ConnectionPool(host=host, port=port, db=db,password = pwd)
#        self.redis = redis.Redis(connection_pool = pool)
        self.redis= redis.Redis(host=host, port=port, db=db,password = pwd)
        threading.Thread.__init__(self)
    def handleUserdata(self,jsondata):
        print jsondata
        
        self.redis.lrem(jsondata)
    def handleTracdesdata(self,jsondata):
        print jsondata
    
    def handleCopydata(self,jsondata):
        print jsondata
        
    def run(self):
        
        while True:
            account_value = self.redis.rpoppush('social:openaccount')
            trades_value = self.redis.rpop('social:trades')
            copy_value = self.redis.rpop('social:copy')
            
            self.handleUserdata(account_value)
            self.handleTracdesdata(trades_value)
            self.handleCopydata(copy_value)
            if account_value is None and trades_value is None and copy_value is None:
                time.sleep(10)
            
    
    