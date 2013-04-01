#!/usr/bin/env python
#-*-encoding:utf-8-*-

import time
import string
from utils import encrypt_password
from tornado.options import define, options
from tornado.database import Connection,IntegrityError

define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="2057", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="", help="blog database password")

class BaseModel(object):

    
    def __init__(self):
        
        self.db = Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

    @classmethod
    def instance(cls):
        
        if not hasattr(cls,'_instance'):
            cls._instance=cls()
        return cls._instance

class UserModel(BaseModel):
    
    
    def check_email_is_not_exists(self, email):
        
        sql = "select count(email) as count from users where email = %s;"
        res = self.db.get(sql,email)
        if res['count'] > 0:
            return False
        return True
    
    def check_nickname_is_not_exists(self, nickname):
        
        sql = "select count(nickname) as count from users where nickname = %s;"
        res = self.db.get(sql,nickname)
        if res['count'] > 0:
            return False
        return True

    def get_ts_by_email(self, email):
        
        sql = "select UNIX_TIMESTAMP(created) as ts,id,password from users where email = %s;"
        res = self.db.get(sql,email)
        if res:
            return res
        return 

    def register(self, nickname, email, password):
        
        if not self.check_email_is_not_exists(email):
            #TODO return
            return 
        ts = int(time.time())
        db_password = encrypt_password(password,str(ts))
        sql = "insert into users(nickname,email,password) values (%s,%s,%s);"
        try:
            user_id = self.db.execute_lastrowid(sql,nickname,email,db_password)
            return user_id
        except Exception,e:
            return 
        
    def login(self, email, password):
        
        res = self.get_ts_by_email(email)
        if not res:
            return 
        ts,user_id,db_password = res['ts'],res['id'],res['password']
        password = encrypt_password(password,str(ts))
        if password == db_password:
            return user_id
        return 

    def get(self, user_id):

        sql = "SELECT * from users where id = %s;"
        res = self.db.get(sql, user_id)
        return res

    def batch_get(self, user_ids):
        res = self.db.query("SELECT * from users where id in (" +",".join(["%s"] * len(user_ids)) + ")", *user_ids)
        return res

class NoteModel(BaseModel):

    
    def create(self, title, content, author_id):
        
        slug_base = title.replace(" ", "-").lower()
        valid_letters = string.ascii_letters + string.digits + "-"
        slug_base = "".join(c for c in slug_base if c in valid_letters)[:90]
        tries = 0
        while True:
            try:
                slug = slug_base + "-" + str(tries) if tries > 0 else slug_base
                sql = "INSERT INTO notes (title,slug,author_id,content,created) VALUES (%s,%s,%s,%s,DATE_ADD( UTC_TIMESTAMP( ) , INTERVAL 8 HOUR ))"
                return self.db.execute_lastrowid(sql, title, slug,author_id, content)
            except IntegrityError:
                tries += 1

    def update(self):
        pass

    def delete(self):
        pass

    def get(self, note_id):
        
        sql = "SELECT * from notes where id = %s;"
        res = self.db.get(sql,note_id)
        return res

    def batch_get(self, author_ids, page):
        if not page:
            page = 1
        page = int(page)
        sql = "SELECT * from notes where author_id in %s order by id desc limit 20 offset %s;"
        res = self.db.query(sql,tuple(author_ids),(page-1)*20)
        return res

    def get_note_count(self, user_id):
        sql = "select count(author_id) as count from notes where author_id=%s;"
        res = self.db.get(sql, user_id)
        return res['count']

    def get_user_note(self, user_id):
        sql = "SELECT * from notes where author_id=%s order by id desc;"
        res = self.db.query(sql,user_id)
        if len(res) > 0:
            return res
        return None

    def get_recent_notes(self):
        sql = "SELECT id,title from notes order by id desc limit 5;"
        res = self.db.query(sql)
        if len(res) > 0:
            return res
        return None

class CommentModel(BaseModel):


    def create(self, note_id, user_id, content, parent_id=None):
        
        if not parent_id:
            parent_id=0
        sql = "INSERT INTO comments (user_id,note_id,parent_id,content,created) VALUES (%s,%s,%s,%s,DATE_ADD( UTC_TIMESTAMP( ) , INTERVAL 8 HOUR ));"
        try:
            return self.db.execute(sql,user_id,note_id,parent_id,content)
        except Exception:
            import sys
            print sys.exc_info()
            return False

    def update(self):
        
        pass

    def delete(self):
        
        pass

    def get(self, comment_id):

        sql = "SELECT * from comments where id = %s;"
        res = self.db.query(sql,comment_id)
        if len(res)>0:
            return res
        return 

    def batch_get(self, note_id):

        sql = "SELECT a.created,a.content,a.id,b.avatar,b.nickname from comments a left join users b on a.user_id = b.id where note_id = %s order by a.id desc;"
        res = self.db.query(sql,note_id)
        if len(res)>0:
            return res
        return 

class RelationModel(BaseModel):

    def is_follow(self, user_id, other_user_id):

        sql = "select count(from_user_id) as count from relations where from_user_id = %s and to_user_id = %s;"
        res = self.db.get(sql,user_id,other_user_id)
        if res.get("count")>0:
            return True
        return False

    def add_follow(self, from_user_id, to_user_id):
        sql = "insert into relations(from_user_id,to_user_id,created) values(%s,%s,DATE_ADD( UTC_TIMESTAMP( ) , INTERVAL 8 HOUR ))"
        res = self.db.execute_rowcount(sql,from_user_id,to_user_id)
        return res==1

    def remove_follow(self, from_user_id, to_user_id):
        sql = "delete from relations where from_user_id=%s and to_user_id=%s;"
        res = self.db.execute_rowcount(sql,from_user_id,to_user_id)
        return res==1

    def get_friend_ids(self, user_id):

        sql = "select to_user_id from relations where from_user_id = %s;"
        res = self.db.query(sql,user_id)
        if len(res)>0:
            return [item['to_user_id'] for item in res]
        return

    def get_fans_ids(self, user_id):
        sql = "select from_user_id from relations where to_user_id = %s;"
        res = self.db.query(sql,user_id)
        if len(res)>0:
            return [item['from_user_id'] for item in res]
        return

    def get_friend_count(self, user_id):
        sql = "select count(to_user_id) as count from relations where from_user_id = %s;"
        res = self.db.get(sql,user_id)
        return res['count']

    def get_fans_count(self, user_id):
        sql = "select count(from_user_id) as count from relations where to_user_id = %s;"
        res = self.db.get(sql,user_id)
        return res['count']

    def get_relation_status(self, user_id, other_user_id):
        if self.is_follow(user_id,other_user_id) and self.is_fans(user_id,other_user_id):
            #TODO 互相关注
            return {'relation_status':1}
        if self.is_follow(user_id,other_user_id):
            #TODO 已关注
            return {'relation_status':2}
        if self.is_fans(user_id,other_user_id):
            #TODO 粉丝
            return {'relation_status':3}
        return {'relation_status':4}

    def is_fans(self, user_id, other_user_id):

        sql = "select count(from_user_id) as count from relations where from_user_id = %s and to_user_id = %s;"
        res = self.db.get(sql,other_user_id,user_id)
        if res.get("count")>0:
            return True
        return False



class NotificationModel(BaseModel):

    def add_notification(self, from_user_id, to_user_id, message, notify_type, note_id=None):

        sql = "insert into notifications(from_user_id,to_user_id,message,notify_type,note_id,created) values (%s,%s,%s,%s,%s,DATE_ADD( UTC_TIMESTAMP( ) , INTERVAL 8 HOUR ));"
        try:
            return self.db.execute(sql,from_user_id,to_user_id,message,notify_type,note_id)
        except Exception:
            return False
        
    def get_notification(self, user_id):
        #TODO since_id,max_id
        sql = "select from_user_id,to_user_id,message,notify_type,created,note_id from notifications where to_user_id = %s order by created desc;"
        res = self.db.query(sql,user_id)
        if len(res)>0:
            return res
        return None

def main():
    relation = RelationModel()
#    res = relation.add_follow(4,3)
    res = relation.get_friend_ids(4)
    print res

if __name__ == "__main__":
    main()
