# -*- coding:utf8 -*-
'''
Created on 2015-1-6

@author: fuwenbin
'''
import urllib
import urllib2
import httplib
import json

def testpusblishtopic():
    "发表主题"
    
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'publisher_id':8089,
                       'content':"这周末是美国非农时间，所以我觉得可以做多美1203元，强烈推荐做空 $EURUSD ，大家赶紧跟我买啊，想赚钱的赶紧跟我单。机不可失，失不再来。",
                       'bytramsmitid':0
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/publishtopic",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
    
def testgetselfrelationinfos():
    "获取与某人相关的主题信息"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'usercode':1120,
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/relataiontopic",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status

def testtopicdetail():
    "获取话题的详细信息"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'topic_id':1120,
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/topicdetail",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status

def testgethotinvesterinfo():
    "获取热门投资者话题信息"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'startindex':0,
                       'offset':10,
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/hotinvester",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
def testgetfansinfomation():
    """获取粉丝信息"""
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'usercode':1120,
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/attentionsfans",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
def testdotopicsupport():
    "主题（或者评论）点赞"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'type':1,
                       'usercode':1205,
                       'topicid':3
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/dosupportpoint",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
def testdocomment():
    "评论"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'type':0,
                       'usercode':1203,
                       'content':"good luck",
                       'topicid':1002
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/docomment",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
def testdofans():
    "关注"
    headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = httplib.HTTPConnection("127.0.0.1:5002")
    requestJsondata = {
                       'usercode':8089,
                       'by_attention_id':1120
                       }
    data = json.dumps(requestJsondata,encoding = 'utf-8')
    conn.request("POST","/communicate/api/doattention",data,headers)
    response = conn.getresponse()
    if response.status ==200:
        print "everytings is ok"
    else:
        print response.reason,response.status
    
    
    
if __name__== '__main__':
#    testpusblishtopic()
#    testgetfansinfomation()
#    testdocomment()
#    testdofans()
#    testdotopicsupport()
    testgethotinvesterinfo()