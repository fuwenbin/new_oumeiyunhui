'''
Created on 2015-1-8

@author: fuwenbin
'''
import sys
import traceback

class Errors(object):
    
    @staticmethod
    def TraceErrorHandler(self):
        etype,evalue,tracebackObj = sys.exc_info()[:3]
        print "Type:",etype
        print "Value:",evalue
        traceback.print_tb(tracebackObj)