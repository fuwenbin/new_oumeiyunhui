'''
Created on 2014-12-31

@author: fuwenbin
'''
from db.mydb import MyDB
from tornado.escape import json_decode,json_encode
import logging
class Processor():
    ''' this is handler's super class'''
    def __init__(self,requesthandler):
        self.handler = requesthandler
#        if requesthandler.request.body is not '':
#            jsonbody = json_decode(requesthandler.request.body)
#        self.redis = requesthandler.applicatoin.redis
#            self.jsonbody= jsonbody
        self.mydb = MyDB(requesthandler.application.conn)
            
    def _response_data(self,data):
        print "jsondata is :%s"%json_encode(data)
#        logging.debug("jsondata is %s",json_encode(data))
#        self.handler.add_header("Access-Control-Allow-Origin","*");
        self.handler.write(json_encode(data))
        
    def dowork(self):
        raise NotImplementedError
    
    def response_success(self,data=''):
        rdata={"statecode":1,
              "statemessage":'successful!!!',
              "data":data
              }
        self._response_data(rdata)
        
    def response_fail(self,message):
        data={"statecode":0,"statemessage":message}
        self._response_data(data)