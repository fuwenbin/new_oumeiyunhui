# -*- coding:utf-8 -*-
'''
Created on 2014-12-29

@author: fuwenbin
'''
import tornado.web
from hotinvester import HotInvester
from attentionsomebody import AttentionSomeBody
from comment import Comment
from getattionandfans import GetAttentionAndFansInfo
from getrelationinfos import GetRelationInfos
from getinfomation import GetInfomation
from publishtopic import PublishTopic
from topicdetail import TopicDetail
from support import Support
from utils.errors import Errors
from tornado.web import HTTPError

class BaseHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        pass
#        tornado.web.RequestHandler.set_default_headers(self)
#        self.set_header('Access-Control-Allow-Origin', 'http://192.168.1.59:9000')
#        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
#        self.set_header('Access-Control-Max-Age', 1000)
#        self.set_header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept , If-Modified-Since')
#        self.set_header('Access-Control-Allow-Headers', 'If-Modified-Since')
#        self.set_header('If-Modified-Since', 0)
#        self.set_header('Content-type', 'application/json')
class MainHandler(BaseHandler):
    
    
    '''this class will handle all request .  it will payout request to the specific handler'''
    @tornado.web.asynchronous
    def post(self, command):
        self.write("hello get method ! server is runging")
        print "requst get command:%s" % command
        self.finish()
    @tornado.web.asynchronous
    def get(self, command):
        print "command is : %s"%command
        
        handler = None
        if command == 'hotinvester_p':
            handler = HotInvester(self)
        elif command == 'publishtopic_p':
            handler = PublishTopic(self)
        elif command == 'topicdetail_p':
            handler = TopicDetail(self)
        elif command == 'attentionsfans_p':
            handler = GetAttentionAndFansInfo(self)
        elif command == 'relationtopic_p':
            handler = GetRelationInfos(self)
        elif command == 'dosupportpoint_p':
            handler = Support(self)
        elif command == 'docomment_p':
            handler = Comment(self)
        elif command == 'doattention_p':
            handler = AttentionSomeBody(self)
        elif command == 'geinformation_p':
            handler = GetInfomation(self)
        else:
            raise HTTPError(status_code=404)
        if handler :
            try:
                handler.dowork()
            except:
                Errors.TraceErrorHandler(self)
                self.write("")##返回空字符串,代表服务器报错
        print "request post"
        self.finish()
    
    def prepare(self):
        """处理跨域请求"""
#        accessl = eval(self.application.config[2])
#        origin = self.request.headers.get("Origin","")
#        accessControlRequestMethod = self.request.headers.get("Access-Control-Request-Method","")
#        if not accessl or  accessl is '' or origin is '' or accessControlRequestMethod is '':
#            return None
#        for access_origin in accessl:
#            if access_origin == origin:
#                self.request.method = accessControlRequestMethod
#        return None


