# -*- coding:utf-8 -*-
'''
Created on 2015年4月7日

@author: fuwenbin
'''

import torndb
import logging
from utils.filters import filterplaceholder
class MyConnection(torndb.Connection):
    def __init__(self,hostaddress,db,user,password,timeout):
        
        torndb.Connection.__init__(self,hostaddress,db,user,password,connect_timeout = timeout,time_zone = '+8:00')
    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            filterParameters = []
            if parameters:
                for param in parameters:
                    if isinstance(param,str):
                        filterParameters.append(filterplaceholder(param))
                    else:
                        filterParameters.append(param)
            filterkwparameters = {}
            if kwparameters:
                for k,v in kwparameters.items():
                    if isinstance(v, str):
                        filterkwparameters[k] = filterplaceholder(v)
                    else:
                        filterkwparameters[k] = v
                    
            return cursor.execute(query, filterParameters or filterkwparameters)
        except torndb.MySQLdb.OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host)
            self.close()
            raise