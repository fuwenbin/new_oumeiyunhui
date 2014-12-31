#-*- coding: utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''


import tornado.ioloop
import tornado.web
from tornado import httpserver
import time
import logging
from handler.mainhandler import MainHandler

class MyApplication(tornado.web.Application):
    """application init here"""
    
    def __init__(self,mysqlconfig,redisconfig):
        
        starttime = time.time()
        
        handlers = [
                    (r"/",MainHandler),#
                    ]
        
        settings = dict(gzip= True,
                       debug = False)
        self.conn = initConnectToMysql(*mysqlconfig)
        tornado.web.Application.__init__(self,handlers=handlers,**settings)
        
def initConfigParams():
    from ConfigParser import ConfigParser        
    parser = ConfigParser()
    parser.read('serverconfig.cfg')
    server_port = parser.get('default','server_port')
    log_path = parser.get('default','log_path')
    
    mysql_address = parser.get('mysql','host')
    mysql_user = parser.get('mysql','user')
    mysql_pwd = parser.get('mysql','pwd')
    
    redis_host = parser.get('redis','host')
    redis_port = parser.get('redis','port')
    redis_db = parser.get('redis','db')
    redis_pwd = parser.get('redis','pwd')
    
    return (server_port,log_path),(mysql_address,mysql_user,mysql_pwd),(redis_host,redis_port,redis_db,redis_pwd)

def initConnectToMysql(hostaddress,user,password):
    import torndb
    dbConnected=torndb.Connection(hostaddress,'tiger_communicate',user,password)
    return dbConnected

def initLog(syslogpath):
    logger = logging.getLogger()
    log_handler = logging.handlers.RotatingFileHandler(syslogpath+"/syslog.log",maxBytes = 104857600,backupCount=50)
    formatter = logging.Formatter('[%(asctime)s %(levelname)]s:%(filename)s:%(funcName)s:%(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.NOTSET)
    
def initRedis(host,port,db,pwd):
    from db.redisclient import  RedisReading
    return RedisReading(host=host,port = port,db=db,password=pwd)
    
def main():
    default_config,mysql_config,redis_config = initConfigParams()
    initLog(default_config[1])
    server = httpserver.HTTPServer(MyApplication(mysql_config,redis_config))
    server.bind(default_config[0])
    server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
    """start program here"""
    

