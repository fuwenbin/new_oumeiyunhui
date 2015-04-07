'''
Created on 2015-1-30

@author: fuwenbin
'''

from tornado.web import RequestHandler
class LoginAutheHandler(RequestHandler):
    
    def get(self):
        print "login auth get handler"
        
        self.write("you are not login!!!!")
    
    def post(self):
        print "login auth post handler"
        