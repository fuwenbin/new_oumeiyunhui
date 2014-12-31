'''
Created on 2014-12-31

@author: fuwenbin
'''


class MyDB():
    
    
    '''excute mysql options'''
    
    def __init__(self,conn):
        print 'init MYDB'
        self.conn = conn
    
    
    def saveCopyTopic(self):
        sql_str = 'insert into '
        self.conn.insert(sql_str)
        
    def saveTradeTopic(self):
        
        pass
    