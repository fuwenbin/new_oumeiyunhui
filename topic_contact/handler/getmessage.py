#-*- coding:utf8 -*-
'''
Created on 2015-2-7

@author: fuwenbin
'''
from handler.processor import Processor
import json
class GetMessage(Processor):
    def dowork(self):
        data = json.loads(self.handler.request.body)
        protocal = data['protocal']
        arguments = data['arguments']
        if protocal == 'unvisited':
            self._unVisitedInfo(arguments)
        elif protocal == 'messageInfo':
            self._getMessageInfo(arguments)
        elif protocal == 'visitedMessage':
            self._visitedMessage(arguments)
        elif protocal == 'delMessage':
            self._deleteMessage(arguments)
        elif protocal == 'loadMore':
            self._getMoreMessage(arguments)
        
    def _unVisitedInfo(self,arguments):
        usercode = arguments.get('user_code',0)
        sys_unvisited_sum,user_unvisited_sum = self.mydb.getUnVisitedInfo(usercode)
        unvisited = {}
        unvisited['sys_unvisited_sum'] = sys_unvisited_sum
        unvisited['user_unvisited_sum'] = user_unvisited_sum
        self.response_success(unvisited)
    def _getMessageInfo(self,arguments):
        usercode = self.handler.get_cookie('userCode')
        startindex = arguments.get('start_index',0)
        offset = int(arguments.get('offset',10))
        data = {}
        sys_unvisited_sum,user_unvisited_sum = self.mydb.getUnVisitedInfo(usercode)
        unvisited = {}
        unvisited['sys_unvisited_sum'] = sys_unvisited_sum
        unvisited['user_unvisited_sum'] = user_unvisited_sum
        data['unvisited_sum'] = unvisited
        
        sys_msgs,user_msgs = self.mydb.getMessage(usercode, startindex, offset)
        data['sys'] = sys_msgs
        data['user'] = user_msgs
        
        self.response_success(data)
    def _visitedMessage(self,arguments):
        message_ids = arguments.get('message_ids',[])
        typeS = arguments.get('type')
        userCode = self.handler.get_cookie('userCode',0)
        if typeS =='sys':
            for msgId in message_ids:
                self.mydb.updateSysMessage(userCode, msgId)
            self.handler.set_cookie('sys_unvisited_sum',str(0))
        else:
            for msgId in message_ids:
                self.mydb.updateUserMessage(userCode, msgId)
            self.handler.set_cookie('user_unvisited_sum',str(0))
        self.response_success("good!")
    def _deleteMessage(self,arguments):
        userCode = self.handler.get_cookie('userCode',0)
        typeS = arguments.get('type')
        messageId = arguments.get('message_id')
        if typeS =='sys':
            self.mydb.delSysMessage(userCode,messageId)
        else:
            self.mydb.delUserMessage(userCode, messageId)
        self.response_success("good ")
    def _getMoreMessage(self,arguments):
        startIndex = arguments.get('start_index')
        userCode = self.handler.get_cookie('userCode',0)
        typeS = arguments.get('type')
        offset = arguments.get('offset')
        if typeS=='sys':
            self._getMoreSysMessage()
        else:
            self._getMoreUserMessage()
            