'''
Created on 2015-1-29

@author: fuwenbin
'''

from processor import Processor

class GetFansSum(Processor):
    
    def dowork(self):
        try:
            usercodes = eval(self.handler.get_argument('usercodes',[]))
        except:
            self.response_fail("argument error!!!")
        response_data = []
        for usercode in usercodes:
            m = {}
            sum = self.mydb.getFansSum(usercode)
            m[usercode] = sum
            response_data.append(m)
        self.response_success(response_data)