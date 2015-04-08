# -*- coding: utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''


import tornado.ioloop
import tornado.web
from tornado import httpserver
import time
import logging
import logging.handlers
from handler.mainhandler import MainHandler
from handler.loginauthhandler import LoginAutheHandler
import sys
reload(sys)   
sys.setdefaultencoding('utf8') 
class MyApplication(tornado.web.Application):
    """application init here"""
    
    def __init__(self,conn,defaultconfig):
        
        start = time.time()
        
        handlers = [
                    (r"/communicate/api/([a-z]+)",MainHandler),
                    (r"/login_url",LoginAutheHandler)
                    ]
        
        settings = dict(gzip= True,
                       debug = False,
                       xsrf_cookies=False,
                       cookie_secret="YXRvbS50cmFkZSBpcyB0aGUgYmVzdAo=",
                       login_url="/login_url")
        self.conn = conn
        tornado.web.Application.__init__(self,handlers=handlers,**settings)
#        self.add_handlers("http://192.168.1.59:5002", handlers)
        end = time.time()
        self.config = defaultconfig
        logging.info("...starting server for time:"+str((end-start)*1000)+u"毫秒")
        print("...starting server for time:"+str((end-start)*1000)+u"毫秒")
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
    from db.myconnection import MyConnection
    dbConnected=MyConnection(hostaddress,'tiger_communicate',user,password,1000)
    return dbConnected

def initLog(syslogpath):
    import os 
    if not os.path.exists(syslogpath):
        os.mkdir(syslogpath)
    
    logger = logging.getLogger()
    log_handler = logging.handlers.RotatingFileHandler(syslogpath+"/syslog.log",maxBytes = 104857600,backupCount=50)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(filename)s:%(funcName)s:%(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.NOTSET)
    
def initRedisThread(host,port,db,pwd):
    from db.redisclient import  getDataFromRedis
    return getDataFromRedis(host,port,db,pwd)
    
def main():
    default_config,mysql_config,redis_config = initConfigParams()
    initLog(default_config[1])
    conn = initConnectToMysql(*mysql_config)
    
    from db.redisclient import  getDataFromRedis
    data = getDataFromRedis(*(redis_config+(conn,)))
    data.startGetData()
    
    server = httpserver.HTTPServer(MyApplication(conn,default_config))
    server.bind(default_config[0])
    server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
    """start program here"""
    

