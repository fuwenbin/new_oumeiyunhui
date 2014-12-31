# -*- coding:utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    
    '''this class will handle all request .  it will payout request to the specific handler'''
    @tornado.web.asynchronous
    def get(self):
        self.request.write("hello get method ! server is runging")
    
    @tornado.web.asynchronous
    def post(self):
        self.request.write("hello post method ! server is runging")