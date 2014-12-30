#-*- coding: utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''


import tornado.ioloop
import tornado.web
import time
from handler.mainhandler import MainHandler

class Appliaction(tornado.web.Application):
    
    def __init__(self):
        
        starttime = time.time()
        
        handlers = [
                    (r"/",MainHandler),
                    ]
        
        settings = dict(gzip= True,
                       debug = False)
    
        tornado.web.Application.__init__(self,handlers=handlers,**settings)
        
        
        


if __name__ == '__main__':
    
    """start program here"""
    

