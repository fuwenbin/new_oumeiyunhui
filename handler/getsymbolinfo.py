#-*- coding:utf8 -*-
'''
Created on 2015-1-31

@author: fuwenbin
'''
from processor import Processor
from compiler import symbols
import time
from utils.filters import filterSensitive
class GetSymboInfo(Processor):

	def dowork(self):
		
		symbol = self.handler.get_argument('symbol')
		startIndex = self.handler.get_argument('startIndex')
		topiclist = self.mydb.getSymbolInfo(symbol,startIndex)
		topic_data = []
		for row in topiclist:
			row['ptime'] = int(time.time()) - int(time.mktime(time.strptime(row['ctime'], "%Y-%m-%d %H:%M:%S")))
			topicType = row['topic_type']
			if row['content']:
				row['content'] = filterSensitive(row['content'])
			if topicType == 0:
				pass
			elif topicType ==1: # closeout
				closeoutinfo = self.mydb.getcloseoutTopicInfo(row['relation_key'])
				row['relation'] = closeoutinfo
			elif topicType == 2: # copy 
				copyinfo = self.mydb.getcopyTopicInfo(row['relation_key'])
				copyinfo['be_follow_sum'] = row.content
				row['relation'] = copyinfo
			elif topicType == 3:  #tramsmit 
				tramsmit_id = row.tramsmit_id
				byTramsmit_topicinfo = self.mydb.getTopicInfo(tramsmit_id)   
				byTramsmit_topicinfo['ptime'] = time.time()-time.mktime(time.strptime(byTramsmit_topicinfo['ctime'], "%Y-%m-%d %H:%M:%S"))
				row['relation'] = byTramsmit_topicinfo
			topic_data.append(row)
		self.response_success(topic_data)