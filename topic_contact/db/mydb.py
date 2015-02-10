# -*- coding:utf-8 -*-
'''
Created on 2014-12-31

@author: fuwenbin
'''
from utils.filters import filterSqlSpecialWord

class MyDB():
    
    
    '''excute mysql options'''
    
    def __init__(self,conn):
        self.conn = conn
    
    def saveCopyTopic(self):
        sql_str = 'insert into '
        self.conn.insert(sql_str)
        
    def saveTradeTopic(self):
        
        pass
    
    def getusername(self,usercode):
        
        return self.conn.get("select username from user_info where userid = %s",usercode).username
        
    
    def publishtopic(self,params):
        sql_str = """insert into topic_communicate_info(publisher_id,publisher_name,content,topic_type,relation_key,ctime,is_public)
        values(%(publisherid)s,%(publishername)s,%(content)s,%(topictype)s,%(relationkey)s,%(ctime)s,%(ispublic)s)
        """
        return self.conn.insert(sql_str,
                                publisherid = params['publisherid'],
                                publishername = params['publishername'],
                                content = filterSqlSpecialWord(params['content']),
                                topictype = params['topictype'],
                                relationkey = params['relationkey'],
                                ctime = params['ctime'],
                                ispublic = params['ispublic']
                                )
        
    def getPublicTopic(self,startindex=0,offset=10):
        
        sql_str = """select topicid,publisher_id,publisher_name,content,topic_type,relation_key,
            DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%i:%%s') as ctime ,
            (select count(by_topicid) from tramsmit_rel where by_topicid = w.topicid) as tramsmit_sum,
            (select count(supporter_id) from topic_support_rel where by_topicid = w.topicid) as support_sum,
            (select count(comment_id) from comment_info where by_topicid = w.topicid) as comment_sum
            from topic_communicate_info w where is_public = 1 and state = 1 order by topicid desc limit %s,%s"""

        results = self.conn.query(sql_str,startindex,offset)
        return results
    
    def getRelationInfo(self,usercode,startindex,offset=10):
        sql_str = """select topicid,publisher_id,publisher_name,content,topic_type,relation_key,
            DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') as ctime ,
            (select count(by_topicid) from tramsmit_rel where by_topicid = w.topicid) as tramsmit_sum,
            (select count(supporter_id) from topic_support_rel where by_topicid = w.topicid) as support_sum,
            (select count(comment_id) from comment_info where by_topicid = w.topicid) as comment_sum
            from topic_communicate_info w where publisher_id = %s and state = 1 order by topicid desc limit %s,%s
        """%(usercode,startindex,offset)
        return self.conn.query(sql_str)
    
    def getTopicSupportSum(self,topicid):
        
        sql_str = "select count(supporter_id) sum from support_rel where by_topicid = %s"
        
        entity = self.conn.get(sql_str,topicid)
        return entity.sum
    
    def getTopicCommentSum(self,topicid):
        '''获取被评论的topic的评论数'''
        sql_str = "select count(comment_id) sum from comment_rel where by_topicid = %s and by_comment_id=0"
        entity = self.conn.get(sql_str,topicid)
        return entity.sum
    
    def getTopicTramsmitSum(self,topicid):
        '''获取转发数量'''
        sql_str = "select count(by_topicid) sum from tramsmit_rel where by_topicid = %s"
        entity = self.conn.get(sql_str,topicid)
        return entity.sum
    
    def getTopicOfCommentLevel1(self,topicid,startindex,offset = 10):
        """获取对指定主题的直接所有评论"""
        sql_str = """select w.comment_id,w.comment_publisherid,
        (select username from user_info where userid = w.comment_publisherid) as publisher_name,
        w.by_topicid,w.by_comment_id,w.content,
        DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime, 
        (select count(supporter_id) from comment_support_rel where by_commentid = w.comment_id) as support_sum,
        (select count(comment_id) from comment_info where by_comment_id = w.comment_id) as comment_sum
        from comment_info w where w.by_topicid =%s and w.by_comment_id=0 and w.state = 1"""%topicid
        
   
        sql_str = sql_str + " order by w.comment_id desc limit %s,%s"%(startindex,offset)

        
        return self.conn.query(sql_str)
    
    def getTopicOfCommentLevel2(self,bycommentid,startIdOrIndex=0,offset=3):
        """获取对主题的评论的相关2级评论"""
        sql_str = """select w.comment_id,w.comment_publisherid,w.by_topicid,w.by_comment_id,w.content,
        DATE_FORMAT(w.ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime,
        (select username from user_info where userid = w.comment_publisherid) as publisher_name,
        (select count(supporter_id) from comment_support_rel where by_commentid = w.comment_id) as support_sum
        from comment_info w where w.by_comment_id=%s and w.state = 1"""%(bycommentid)
        
        if startIdOrIndex>0:
            sql_str = sql_str + " and comment_id < %s"%startIdOrIndex
            sql_str = sql_str + " order by w.comment_id desc"
        else:
            sql_str = sql_str + " order by w.comment_id desc"
            sql_str = sql_str + " limit %s,%s"%(startIdOrIndex,offset)
        
        return self.conn.query(sql_str)
    
    def getcloseoutTopicInfo(self,closeoutid):
        '''获取平仓信息'''
        sql_str = """select c.usercode,u.username,c.closeout_id,c.out_type,c.profit_point 
        from closeout_topic c left join user_info u on c.usercode = u.userid
        where c.closeout_id = %s"""
        return self.conn.get(sql_str,closeoutid)
        
    def getcopyTopicInfo(self,followid):
        '''获取复制信息'''
        sql_str = """select a.follow_id,a.by_follow_id,u1.username byname,a.be_follow_id,u2.username bename 
        from follow_topic a left join user_info u1 on a.by_follow_id = u1.userid 
        left join user_info u2 on a.be_follow_id = u2.userid where a.follow_id = %s
        """
        return self.conn.get(sql_str,followid)
        
    def getcommentInfo(self,commentid):
        '''获取评论信息'''
        sql_str= '''select comment_id,comment_publisherid,by_topicid,by_comment_id,
        content,DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') as ctime,
        (select count(comment_id) from comment_info where by_comment_id = %s) as comment_sum,
        (select count(supporter_id) from comment_support_rel where by_commentid = %s) as support_sum
        from comment_info comment_id = %s join '''
        return self.conn.get(sql_str,commentid,commentid,commentid)
        
        
    def getTopicInfo(self,topicid):
        
        sql_str = '''select topicid,publisher_id,publisher_name,content,topic_type,relation_key,
        DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%i:%%s') as ctime, 
        (select count(by_topicid) from tramsmit_rel where by_topicid = %s) as tramsmit_sum,
        (select count(supporter_id) from topic_support_rel where by_topicid = %s) as support_sum,
        (select count(comment_id) from comment_info where by_topicid = %s) as comment_sum
        from topic_communicate_info where topicid = %s and state = 1'''
        return self.conn.get(sql_str,topicid,topicid,topicid,topicid)
        
    def getfansInfos(self,usercode):
        sql_str = '''select count(fans_id) sum from fans_rel where fans_id = %s'''
        attentionsum = self.conn.get(sql_str,usercode)
        sql_str = '''select count(fans_id) sum from fans_rel where by_attention_id = %s'''
        fanssum = self.conn.get(sql_str,usercode)
        return dict(attention_sum = attentionsum.sum,fans_sum=fanssum.sum)
    
    def attentionOne(self,usercode,attentionid):
        try:
            sql_str = '''insert into fans_rel(fans_id,by_attention_id,ctime) values(%s,%s,now())'''
            self.conn.insert(sql_str,usercode,attentionid)
        except Exception:
            return 1
        return 0
    
    def cancleAttention(self,usercode,attentionid):
        sql_str = '''delete from fans_rel where fans_id =%s and by_attention_id = %s'''%(usercode,attentionid)
        return self.conn.execute_lastrowid(sql_str)    
    
    def commentTopic(self,usercode,topicid,bycommentid,content,ctime):
        sql_str = '''insert into comment_info(comment_publisherid,by_topicid,by_comment_id,content,ctime) values(%s,%s,%s,'%s','%s')'''%(usercode,topicid,bycommentid,filterSqlSpecialWord(content),ctime)
        print sql_str
        return self.conn.insert(sql_str)
        
    def getTopicIdByCommentId(self,commentid):
        sql_str = '''select by_topicid from comment_info where comment_id = %s'''
        topicid =0
        try:
            topicid = self.conn.get(sql_str,commentid).by_topicid
        except:
            return 0
        return topicid
    
    def supportTopic(self,topicid,who):
        
        sql_str = """insert into topic_support_rel (supporter_id,by_topicid,ctime) values(%s,%s,now())"""
        self.conn.insert(sql_str,who,topicid)
        
    def supportComment(self,commentid,who):
        sql_str = """insert into comment_support_rel (supporter_id,by_commentid,ctime) values(%s,%s,now())"""
        self.conn.insert(sql_str,who,commentid)
    
    def deletetopic(self,usercode,topicid):
        sql_str = "update topic_communicate_info set state = 0 where publisher_id = %s and topicid = %s"
        return self.conn.update(sql_str,usercode,topicid)
        
    
    def deletecomment(self,usercode,commentid):
        
        sql_str = '''update table comment_info set state = 0 where comment_publisherid = %s and comment_id = %s'''
        return self.conn.update(sql_str,usercode,commentid)        
    
    def mapconentkey(self,atstr,typekey,relation_key,ctime):
        sql_str = '''insert into atname_rel(atstr,type,relation_key,ctime) values('%s',%s,%s,%s)'''
        return self.conn.insert(sql_str,atstr,typekey,relation_key,ctime)
        
    def maptramsmit(self,bytramsmittopicid,who):
        sql_str = '''insert into tramsmit_rel (by_topicid,who,ctime) values(%s,%s,now())'''
        return self.conn.insert(sql_str,bytramsmittopicid,who)
    
    def getFansSum(self,usercode):
        sql_str = '''select count(id) as sum from fans_rel where by_attention_id = %s'''%usercode
        return self.conn.get(sql_str).sum
    def getAttentionSums(self,usercode):
        pass
    def isFan(self,fans_id,by_attention_id):
        sql_str = '''select count(id) as sum from fans_rel where by_attention_id = %s and fans_id = %s'''%(by_attention_id,fans_id)
        return self.conn.get(sql_str).sum
    def getFansList(self,startindex,offset,usercode):
        sql_str = '''SELECT f.fans_id AS userCode,
                    (SELECT COUNT(fans_id) FROM fans_rel WHERE by_attention_id=f.fans_id) AS fanCount,
                    (SELECT username FROM user_info WHERE userid=f.fans_id) AS userName
                    FROM  fans_rel f
                    WHERE f.by_attention_id = %s limit %s,%s'''%(usercode,startindex,offset)
        return self.conn.query(sql_str)
        
    def getbFansList(self,startindex,offset,usercode):
        sql_str = '''SELECT f.by_attention_id AS userCode,
                    (SELECT COUNT(fans_id) FROM fans_rel WHERE by_attention_id=f.fans_id) AS fanCount,
                    (SELECT username FROM user_info WHERE userid=f.by_attention_id) AS userName
                    FROM  fans_rel f
                    WHERE f.fans_id = %s limit %s,%s'''%(usercode,startindex,offset)
        return self.conn.query(sql_str)
    
    def getMessage(self,usercode,startindex,offset):
        sql_sys_str='''
            SELECT s.id,s.content,DATE_FORMAT(s.ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime,CASE 
            (SELECT 1 FROM msg_visited_rel WHERE rel_id = s.id AND usercode=%s) WHEN 1 THEN 1 ELSE 0 END AS visited
            FROM sys_message s WHERE s.id NOT IN(SELECT rel_id FROM msg_del_rel WHERE usercode=%s) order by id desc limit %s,%s
            '''%(usercode,usercode,startindex,offset)
        sql_user_str='''
                SELECT id,content,DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime,visited,usercode FROM user_message WHERE usercode = %s AND state = 1 ORDER BY id DESC limit %s,%s
                '''%(usercode,startindex,offset)
        sys_msg = self.conn.query(sql_sys_str)
        user_msg = self.conn.query(sql_user_str)
        return sys_msg,user_msg
    def getSysMessage(self,userCode,startIndex,offset):
        sql_sys_str='''
            SELECT s.id,s.content,DATE_FORMAT(s.ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime,CASE 
            (SELECT 1 FROM msg_visited_rel WHERE rel_id = s.id AND usercode=%s) WHEN 1 THEN 1 ELSE 0 END AS visited
            FROM sys_message s WHERE s.id NOT IN(SELECT rel_id FROM msg_del_rel WHERE usercode=%s) order by id desc limit %s,%s
            '''%(userCode,userCode,startIndex,offset)
        return self.conn.query(sql_sys_str)
    
    def getUserMessage(self,userCode,startIndex,offset):
        sql_user_str='''
                SELECT id,content,DATE_FORMAT(ctime,'%%%%Y-%%%%m-%%%%d %%%%H:%%%%i:%%%%s') ctime,visited,usercode FROM user_message WHERE usercode = %s AND state = 1 ORDER BY id DESC limit %s,%s
                '''%(userCode,startIndex,offset)
        return self.conn.query(sql_user_str)
    
    def delSysMessage(self,usercode,msgId):
        sql_str = """insert into msg_del_rel (rel_id,ctime,usercode) values(%s,now,%s)"""%(msgId,usercode)
        return self.conn.insert(sql_str)
    
    def delUserMessage(self,usercode,msgId):
        sql_str = """update user_message set state = 0 where id = %s and usercode=%s"""%(msgId,usercode)
        return self.conn.update(sql_str)
    
    def updateUserMessage(self,usercode,msgId):
        sql_str = """update user_message set visited = 0 where id = % and usercode = %s"""%(msgId,usercode)
        return self.conn.update(sql_str)
    def updateSysMessage(self,usercode,msgId):
        sql_str = """insert into msg_visited_rel (rel_id,ctime,usercode) values(%s,now(),%s)"""%(msgId,usercode)
        return self.conn.insert(sql_str)
    
    def getUnVisitedInfo(self,usercode):
        sys_str = '''SELECT count(s.id) sys_unvisited_sum
            FROM sys_message s WHERE s.id NOT IN
            (SELECT rel_id FROM msg_del_rel WHERE usercode=%s) 
            and s.id not in (select rel_id from msg_visited_rel where s.id = rel_id) '''%usercode
        
        user_str = '''select count(id) user_unvisited_sum from user_message 
        where usercode = %s and state = 1 and visited = 0'''%usercode
        
        return self.conn.query(sys_str)[0].sys_unvisited_sum,self.conn.query(user_str)[0].user_unvisited_sum
        
    
        
        
        
        