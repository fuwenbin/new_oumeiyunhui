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
from followinglist import FollowList
from getfanssum import GetFansSum
from getremaindiscuss import GetRemainDiscuss
from deletetopic import DeleteTopic
from support import Support
from utils.errors import Errors
from tornado.web import HTTPError
import logging

class MainHandler(tornado.web.RequestHandler):
    
    '''this class will handle all request .  it will payout request to the specific handler'''

    @tornado.web.asynchronous
    def post(self, command):
        self.write("hello get method ! server is runging")
        print "requst get command:%s" % command
        self.finish()
#    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, command):
        print "command is : %s"%command
        logging.info("command is : %s",command)
#        print self.get_secure_cookie("user")
        handler = None
        if command == 'hotinvester':
            handler = HotInvester(self)
        elif command == 'publishtopic':
            handler = PublishTopic(self)
        elif command == 'topicdetail':
            handler = TopicDetail(self)
        elif command == 'attentionsfans':
            handler = GetAttentionAndFansInfo(self)
        elif command == 'relationtopic':
            handler = GetRelationInfos(self)
        elif command == 'dosupportpoint':
            handler = Support(self)
        elif command == 'docomment':
            handler = Comment(self)
        elif command == 'doattention':
            handler = AttentionSomeBody(self)
        elif command == 'geinformation':
            handler = GetInfomation(self)
        elif command == 'fanssum':
            handler = GetFansSum(self)
        elif command =='fflist':
            handler = FollowList(self)
        elif command =='getremaindiscuss':
            handler = GetRemainDiscuss(self)
        elif command =='deletetopic':
            handler = DeleteTopic(self)
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
    
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        return user
    



