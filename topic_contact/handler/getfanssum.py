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
        m = {}
        for usercode in usercodes:
            
            sum = self.mydb.getFansSum(usercode)
            m[usercode] = sum
        self.response_success(m)