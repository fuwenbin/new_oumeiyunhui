# -*- coding:utf-8 -*-
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
    
    def getusername(self,usercode):
        
        return self.conn.get("select username from user_info where userid = %S"%usercode)
        
    
    def publishtopic(self,**params):
        sql_str = """insert into topic_communicate_info(publisher_id,publisher_name,content,topic_type,relaiton_key,ctime,is_public)
        values(%(publisherid)s,'%(publishername)'s,'%(content)s',%(topictype)s,%(relationkey)s,now(),%(ispublic)s)
        """
        self.conn.execute(sql_str,params)
        
    def getPublicTopic(self,startindex=0,offset=None):
        
        sql_str = """select topic_id,publisher_name,content,topic_type,relation_key,
            DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%i:%%s') as ctime ,
            (select count(tramsmit_id) from tramsmit_rel where tramsmit_id = w.topic_id) as tramsmit_sum,
            (select count(supporter_id) from topic_support_rel where topic_id = w.topic_id) as support_sum,
            (select count(comment_id) from comment_info where topic_id = w.topic_id) as comment_sum
            from topic_communicate_info w where is_public = 1 order by topic_id desc limit %s,%s"""
        if offset==None:
            offset = 10
        results = self.conn.query(sql_str,startindex,offset)
        return results
    
    def getRelationInfo(self,usercode):
        
        pass
    
    def getTopicSupportSum(self,topicid):
        
        sql_str = "select count(supporter_id) sum from support_rel where topic_id = %s"%topicid
        
        entity = self.conn.get(sql_str)
        return entity.sum
    
    def getTopicCommentSum(self,topicid):
        
        sql_str = "select count(comment_id) sum from comment_rel where by_comment_id = %s and by_comment_id=0"%topicid
        entity = self.conn.get(sql_str)
        return entity.sum
    
    def getTopicTramsmitSum(self,topicid):
        '''获取转发数量'''
        sql_str = "select count(tramsmit_id) sum from tramsmit_rel where tramsmit_id = %s"%topicid
        entity = self.conn.get(sql_str)
        return entity.sum
    
    def getTopicOfCommentLevel1(self,topicid):
        """获取对指定主题的直接所有评论"""
        sql_str = """select w.comment_id,w.comment_publisherid,(select username from user_info where userid = w.comment_publisherid) as publisher_name,w.topic_id,w.by_comment_id,w.content,
        DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%i:%%s') ctime, 
        (select count(supporter_id) from comment_support_rel where topic_id = %s) as support_sum,
        (select count(comment_id) from comment_info where by_comment_id = w.comment_id) as comment_sum
        from comment_info w where w.topic_id =%s and w.by_comment_id=0"""%(topicid,topicid)
        return self.conn.query(sql_str)
    
    def getTopicOfCommentLevel2(self,topicid,commentid):
        """获取对主题的评论的相关2级评论"""
        sql_str = """select comment_id,comment_publisherid,topic_id,by_comment_id,content,DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%i:%%s') ctime,
        (select count(supporter_id) from comment_support_rel where topic_id = %s) as support_sum
        from comment_info where topic_id =%s and by_comment_id=%s"""%(topicid,commentid)
        return self.conn.query(sql_str)
    
    def getcloseoutTopicInfo(self,closeoutid):
        '''获取平仓信息'''
        sql_str = "select closeout_id,out_type,profit_point from closeout_topic where closeout_id = %s"%closeoutid
        return self.conn.get(sql_str)
        
    def getcopyTopicInfo(self,followid):
        '''获取复制信息'''
        sql_str = """select a.follow_id,a.by_follow_id,u1.username byname,a.be_follow_id,u2.username bename 
        from follow_topic a left join user_info u1 on a.by_follow_id = u.userid 
        left join user_info u2 on a.be_follow_id = u.userid where a.follow_id = %s
        """%followid
        return self.conn.get(sql_str)
        
    def getcommentInfo(self,commentid):
        '''获取评论信息'''
        sql_str= '''select comment_id,comment_publisherid,topic_id,by_comment_id,
        content,DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') as ctime,
        (select count(comment_id) from comment_info where by_comment_id = %s) as comment_sum,
        (select count(supporter_id) from comment_support_rel where topic_id = %s) as support_sum
        from comment_info comment_id = %s join '''%(commentid,commentid,commentid)
        return self.conn.get(sql_str)
        
        
    def getTopicInfo(self,topicid):
        
        sql_str = '''select topic_id,publisher_name,content,topic_type,relation_key,
        DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') as ctime, 
        (select count(tramsmit_id) from tramsmit_rel where tramsmit_id = %s) as tramsmit_sum,
        (select count(supporter_id) from topic_support_rel where topic_id = %s) as support_sum,
        (select count(comment_id) from comment_info where topic_id = %s) as comment_sum
        from topic_communicate_info where topic_id = %s '''%(topicid,topicid,topicid)
        return self.conn.get(sql_str)
        
    def getfansInfos(self,usercode):
        sql_str = '''select count(fans_id) sum from fans_rel where fans_id = %s'''%usercode
        attentionsum = self.conn.get(sql_str)
        sql_str = '''select count(fans_id) sum from fans_rel where by_attention_id = %s'''%usercode
        fanssum = self.conn.get(sql_str)
        return dict(attention_sum = attentionsum.sum,fans_sum=fanssum.sum)
    
    def attentionOne(self,usercode,attentionid):
        sql_str = '''insert into fans_rel(fans_id,by_attention_id) values(%s,%s)'''
        self.conn.insert(sql_str,usercode,attentionid)
        
        
    def commentTopic(self,usercode,topicid,bycommentid,content):
        sql_str = '''insert into comment_info(comment_publisherid,topic_id,by_comment_id,content,ctime) values(%s,%s,%s,'%s',now())'''
        self.conn.insert(sql_str)
        
    def getTopicIdByCommentId(self,commentid):
        sql_str = '''select topic_id from comment_info where by_comment_id = %s'''%commentid
        return self.conn.get(sql_str).topic_id
    
    def supportTopic(self,topicid,who):
        
        sql_str = """insert into topic_support_rel (supporter_id,topic_id) values(%s,%s)"""
        self.conn.insert(sql_str,who,topicid)
        
    def supportComment(self,topicid,who):
        sql_str = """insert into comment_support_rel (supporter_id,topic_id) values(%s,%s)"""
        self.conn.insert(sql_str,who,topicid)
    