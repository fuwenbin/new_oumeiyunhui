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
        
    def _unVisitedInfo(self,arguments):
        usercode = arguments.get('user_code',0)
        sys_unvisited_sum,user_unvisited_sum = self.mydb.getUnVisitedInfo(usercode)
        unvisited = {}
        unvisited['sys_unvisited_sum'] = sys_unvisited_sum
        unvisited['user_unvisited_sum'] = user_unvisited_sum
        self.response_success(unvisited)
    def _getMessageInfo(self,arguments):
        usercode = arguments.get('user_code',0)
        startindex = arguments.get('start_index',"")
        offset = int(arguments.get('offset',10))
        
        sys_msgs,user_msgs = self.mydb.getMessage(usercode, startindex, offset)
        sys_unvisited_sum,user_unvisited_sum = self.mydb.getUnVisitedInfo(usercode)
        data = {}
        data['sys'] = sys_msgs
        data['user'] = user_msgs
        unvisited = {}
        unvisited['sys_unvisited_sum'] = sys_unvisited_sum
        unvisited['user_unvisited_sum'] = user_unvisited_sum
        data['unvisited_sum'] = unvisited
        self.response_success(data)
    def _visitedMessage(self,arguments):

        pass
    def _deleteMessage(self,arguments):
        pass