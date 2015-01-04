'''
Created on 2014-12-31

@author: fuwenbin
'''

import redis
import threading
import time
import json
stop_server = False
class RedisReading(threading.Thread):
    '''connect redis to get data !!!'''
    def __init__(self,host,port,db,pwd,mysqlconn):
#        pool = redis.ConnectionPool(host=host, port=port, db=db,password = pwd)
#        self.redis = redis.Redis(connection_pool = pool)
        self.redis= redis.Redis(host=host, port=port, db=db,password = pwd)
        self.conn = mysqlconn
        threading.Thread.__init__(self)
    def handleUserdata(self,jsondata):
        if jsondata is None:
            print "there are no user data !!!!"
            return
        
        map_data = json.loads(jsondata)
        sql_insert = "insert into user_info (userid,username) values (%s,'%s') on duplicate key update username = '%s' "%(map_data['user_code'], map_data['user_name'],map_data['user_name'])
        
        print jsondata
        self.conn.insert(sql_insert)
        self.redis.lrem('social:openaccount',jsondata)
    def handleTracdesdata(self,jsondata):
        if jsondata is None:
            print "there are no tracde data !!!!"
            return
        sql_insert = " "
        map_data = json.loads(jsondata)
        print jsondata
#        self.conn(sql_insert,*map_data.values())
        
        
    
    def handleCopydata(self,jsondata):
        if jsondata is None:
            print "there are no copy data !!!!"
            return
        
        print jsondata
        
    def run(self):
        
        while True:
            account_value = self.redis.rpoplpush('social:openaccount','social:openaccount')
            trades_value = self.redis.rpop('social:trades')
            copy_value = self.redis.rpop('social:copy')
            
            self.handleUserdata(account_value)
            self.handleTracdesdata(trades_value)
            self.handleCopydata(copy_value)
            if account_value is None and trades_value is None and copy_value is None:
                print "there no data in redis , i have to have a rest for ten seconds!!!"
                time.sleep(1)
            
    
    