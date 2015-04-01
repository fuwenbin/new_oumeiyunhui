# -*- coding:utf8 -*-
'''
Created on 2014-12-31

@author: fuwenbin
'''

import redis
import threading
import time
import json
import re
import logging
stop_server = False
from utils.errors import Errors
class getDataFromRedis(object):
    '''connect redis to get data !!!'''
    def __init__(self, host, port, db, pwd, mysqlconn):
        self.redis = redis.Redis(host=host, port=port, db=db, password=pwd)
        self.conn = mysqlconn
    def _handleUserdata(self):
        '''等到用户数据'''
        jsondata = self.redis.brpoplpush('social:openaccount', 'social:openaccount')
        
        logging.info("user_data:"+jsondata)
        if jsondata is None:
            print "there are no user data !!!!"
            return
        map_data = json.loads(jsondata)
        sql_insert = "insert into user_info(userid,username) values (%s,'%s') on duplicate key update username = '%s' " % (map_data['user_code'], map_data['user_name'], map_data['user_name'])
        
        print jsondata
        self.conn.insert(sql_insert)
        self.redis.lrem('social:openaccount', jsondata)
    def _handleTracdesdata(self):
        """
                        得到交易数据
                        
        1000*volume / leverage =  保证金
        
        symbol = 'USDCAD25'  
        
        profit+storage = 盈利
        
                    盈利率 =盈利/保证金
        """
        jsondata = self.redis.blpop('social:trades')
        logging.info("trades_data:"+jsondata)
        if jsondata is None:
            print "there are no closeout data !!!!"
            return
        print jsondata
        map_data = json.loads(jsondata[1])
        if not map_data.has_key('Usercode') :
            return
        usercode = map_data['Usercode']
        if not usercode:
            return
        symbol = map_data['Trade']['symbol']
#        closetime = map_data['Trade']['close_time']
        profit = map_data['Trade']['profit']
        storage = map_data['Trade']['storage']
        volume = map_data['Trade']['volume']
        publisherid = usercode
        
        leverage = re.search(r'\d+',symbol)
        if leverage:
            leverage = int(leverage.group(0))
            symbol = re.sub(r'\d+','',symbol)
        else:
            leverage = 100
        rate = (profit+storage)/(1000*volume/leverage)
        rate = "%.2f"%rate
        sql_str = "insert into closeout_topic(out_type,profit_point,usercode) values('%s',%s,%s)"%(symbol,rate,usercode)
        rowid = self.conn.insert(sql_str)
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        sql_str = "insert into topic_communicate_info (publisher_id,publisher_name,content,topic_type,relation_key,ctime,is_public) values(%s,'%s','%s',%s,%s,'%s',%s)"
        self.conn.insert(sql_str,publisherid,'','',1,rowid,ctime,0)
    
    def _handleCopydata(self):
        '''得到copy数据'''
        
        jsondata = self.redis.brpop('social:copy')
        logging.info("copy_data:"+jsondata)
        if jsondata is None:
            print "there are no copy data !!!!"
            return
        map_data = json.loads(jsondata[1])
        fromcopy = map_data['from']
        to = map_data['to']
        type_copy = map_data['type']
        if type_copy is 'real':
            sql_str = "select count(follow_id).sum from follow_topic where by_follow_id = %s"%fromcopy
            sm = self.conn.get(sql_str).sum
            sql_str = "insert into follow_topic (follow_id,by_follow_id) values(%s,%s)"%(to,fromcopy)
            follow_id = self.conn.insert(sql_str)
            is_public = 0
            if (sm+1)%50==0:
                is_public = 1
            ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            slq_str = "insert into topic_communicate_info (publisher_id,publisher_name,content,topic_type,relation_key,ctime,is_public) values(%s,'%s','%s',%s,%s,'%s',%s)"
            self.conn.insert(slq_str,to,'',sm+1,2,follow_id,ctime,is_public)
            
    def _handeNotification(self):
        '''处理 消息机制'''
         
        jsondata = self.redis.brpop('social:notification')
        logging.info("notify_data:"+jsondata)
        if jsondata is None:
            print "there are no copy data !!!!"
            return
        
        map_data = json.loads(jsondata[1])
        
        sql_str = "insert into sys_message(content,ctime,state,usercode) values(%s,%s,%s,%s)"
        
        
    
    def startGetData(self):
        thread1 = RedisThread();
        thread2 = RedisThread();
        thread3 = RedisThread();
        thread1.addWork(self._handleUserdata)
        thread2.addWork(self._handleTracdesdata)
        thread3.addWork(self._handleCopydata)
        thread1.start()
        thread2.start()
        thread3.start()    
        
class RedisThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def addWork(self,workMethod):
        self.work = workMethod;
    
    def run(self):
        
        while True:
            try:
                self.work() 
            except:
                Errors.TraceErrorHandler(self)
    
    