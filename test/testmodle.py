# -*- coding:utf8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
import urllib
import urllib2
import httplib
import json
import cookielib
from tornado.escape import json_decode

def commucateModelTest(uri,param,hosts ="127.0.0.1:5002"):
    headers = {"Content-type":"application/x-www-form-urlencoded",
               "Accept":"text/plain",
               "Cookie":"userCode = 1204"}
    conn = httplib.HTTPConnection(hosts)
    data = urllib.urlencode(param)
#    data = json.dumps(param,encoding = 'utf-8')
    conn.request("GET","/communicate/api/"+uri,data,headers)
    response = conn.getresponse()
#    if response.status == 200:
    print "command:%s"%uri
    print "request:%s"%data
    rdata = response.read()
    print "response:%s"%rdata 

def trasformDict(dictobj):
    
    paramstr = '';
    for k,v in dictobj.items():
        paramstr = paramstr+"="+v+"&";
    paramstr = paramstr[:-1]
    return urllib.urlencode(paramstr)

def testpusblishtopic():
    "发表主题"
    requestJsondata = {
                       'publisher_id':8089,
                       'content':"this is a test word!!!",
                       'bytramsmitid':0
                       }
    commucateModelTest('publishtopic',requestJsondata)
def testgetrelationinfos():
    "获取与某人相关的主题信息"
    requestJsondata = {
                       'usercode':1120,
                       'startindex':0,
                       'offset':10
                       }
    commucateModelTest('relationtopic',requestJsondata)

def testtopicdetail():
    "获取话题的详细信息"
    requestJsondata = {
                       'topic_id':1000,
                       }
    commucateModelTest('topicdetail',requestJsondata)

def testgethotinvesterinfo():
    "获取热门投资者话题信息"
    requestJsondata = {
                       'startindex':0,
                       'offset':10,
                       }
    commucateModelTest('hotinvester',requestJsondata)
def testgetfansinfomation():
    """获取粉丝信息"""
    requestJsondata = {
                       'usercode':1120,
                       }
    commucateModelTest('attentionsfans',requestJsondata)
def testdotopicsupport():
    "主题（或者评论）点赞"
    requestJsondata = {
                       'type':1,
                       'usercode':1205,
                       'topicid':3
                       }
    commucateModelTest('dosupportpoint',requestJsondata)
def testdocomment():
    "评论"
    requestJsondata = {
                       'type':0,
                       'usercode':1203,
                       'content':"good luck!!!!",
                       'topicid':1009
                       }
    commucateModelTest('docomment',requestJsondata)
def testdofans():
    "关注"
    requestJsondata = {
                       'usercode':8089,
                       'by_attention_id':1206,
                       'action':1
                       }
    commucateModelTest('doattention',requestJsondata)
    
def tesgetFansSum():
    requestJsondata = {
                   'usercodes':['1203','1204','1120','8086','8087','8089','1120','23098'],
                   }
    commucateModelTest('fanssum',requestJsondata,hosts='test.tigerwit.com')
    
def testgetFansInfoLists():
    requestjsondata = {
                    'startIndex':0,
                    'offset':10,
                    'userCode':23703,
                    'type':0
                       }
    commucateModelTest('fflist',requestjsondata)
    
def testMessage():
    headers = {"Content-type":"application/x-www-form-urlencoded",
               "Accept":"text/plain",
               "Cookie":"userCode = 1204"}
    conn = httplib.HTTPConnection('127.0.0.1:5002')
    param ={
            'protocal':'messageInfo',
            'arguments':{
                         'user_code':23765,
                         'start_index':0,
                         'offset':10
                     }
            }
    str_data = json.dumps(param)
#    data = urllib.urlencode(param)
    conn.request("POST","/communicate/api/message",str_data,headers)
    response = conn.getresponse()
    #    print "request:%s"%data
    rdata = response.read()
    print "response:%s"%rdata    

class fortest(object):
    
    
    def fortestDef(self,*params):
        print params
        print locals()
        print self.__dict__
    def __getattribute__(self,name):
        print name
        return object.__getattribute__(self,name)
        
if __name__== '__main__':
#    testpusblishtopic()
#    testgetfansinfomation()
#    testdocomment()
    testdofans()
#    testdotopicsupport()
#    testgethotinvesterinfo()
#    testtopicdetail()
#    testgetrelationinfos()
#    testgetFansInfoLists()
#    testMessage()
#    obj = fortest()
#    obj.fortestDef('[','asdfasdf',']')

