# -*- coding:utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''
import tornado.web
from tornado.escape import json_decode
from handler.hotinvester import HotInvester
class MainHandler(tornado.web.RequestHandler):
    
    '''this class will handle all request .  it will payout request to the specific handler'''
    @tornado.web.asynchronous
    def get(self,command):
        self.write("hello get method ! server is runging")
        print "requst get command:%s"%command
        self.finish()
    @tornado.web.asynchronous
    def post(self,command):
        handler = None
        if command == 'hotinvester':
            handler = HotInvester(self)
        elif command == '':
            pass
        
        if not handler :
            handler.dowork()
#        self.write("hello post method ! server is runging")
        print "request post"
        self.finish()
