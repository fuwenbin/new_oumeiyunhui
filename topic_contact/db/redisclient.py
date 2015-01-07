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
    def __init__(self, host, port, db, pwd, mysqlconn):
#        pool = redis.ConnectionPool(host=host, port=port, db=db,password = pwd)
#        self.redis = redis.Redis(connection_pool = pool)
        self.redis = redis.Redis(host=host, port=port, db=db, password=pwd)
        self.conn = mysqlconn
        threading.Thread.__init__(self)
    def handleUserdata(self, jsondata):
        if jsondata is None:
            print "there are no user data !!!!"
            return
        map_data = json.loads(jsondata)
        sql_insert = "insert into user_info(userid,username) values (%s,'%s') on duplicate key update username = '%s' " % (map_data['user_code'], map_data['user_name'], map_data['user_name'])
        
        print jsondata
        self.conn.insert(sql_insert)
        self.redis.lrem('social:openaccount', jsondata)
    def handleTracdesdata(self, jsondata):
        if jsondata is None:
            print "there are no tracde data !!!!"
            return
        sql_insert = "insert into  "
        map_data = json.loads(jsondata)
        symbol = map_data['symbol']
        closetime = map_data['close_time']
        profit = map_data['profit']
        storage = map_data['storage']
        
        print jsondata
#        self.conn(sql_insert,*map_data.values())
        
        
    
    def handleCopydata(self, jsondata):
        if jsondata is None:
            print "there are no copy data !!!!"
            return
        map_data = json.loads(jsondata)
        fromcopy = map_data['from']
        to = map_data['to']
        type_copy = map_data['type']
        if type_copy is 'real':
            sql_str = "select count(follow_id).sum from follow_topic where by_follow_id = %s"%fromcopy
            sm = self.conn.get(sql_str).sum
            sql_str = "insert into follow_topic (follow_id,by_follow_id) values(%s,%s)"%(to,fromcopy)
            follow_id = self.conn.insert(sql_str)
            if (sm+1)%50==0:
                slq_str = "insert into topic_communicate_info (publisher_id,publisher_name,content,topic_type,relation_key,ctime,is_public) values(%s,'%s','%s',%s,%s,now(),%s)"
                self.conn.insert(slq_str,to,'',sm+1,2,follow_id,1)
    def run(self):
        
        while True:
            account_value = self.redis.rpoplpush('social:openaccount', 'social:openaccount')
            trades_value = self.redis.rpop('social:trades')
            copy_value = self.redis.rpop('social:copy')
            
            self.handleUserdata(account_value)
            self.handleTracdesdata(trades_value)
            self.handleCopydata(copy_value)
            if account_value is None and trades_value is None and copy_value is None:
                print "there no data in redis , i have to have a rest for one seconds!!!"
                time.sleep(1)
            
    
    