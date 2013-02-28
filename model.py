#!/usr/bin/env python
#-*-encoding:utf-8-*-

import time
from util import encrypt_password
from tornado.options import define, options
from tornado.database import Connection

define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="2057", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="", help="blog database password")

db = Connection(host=options.mysql_host, database=options.mysql_database,user=options.mysql_user, password=options.mysql_password)

class BaseModel:
    def __init__(self):
        self.db = db

class UserModel(BaseModel):
    
    def check_email_is_not_exists(self, email):
        sql = "select count(email) as count from user where email = %s;"
        res = self.db.get(sql,email)
        if res['count'] > 0:
            return False
        return True
    
    def check_nickname_is_not_exists(self, nickname):
        sql = "select count(nickname) as count from user where nickname = %s;"
        res = self.db.get(sql,nickname)
        if res['count'] > 0:
            return False
        return True

    def get_ts_by_email(self, email):
        sql = "select UNIX_TIMESTAMP(created) as ts,id from user where email = %s;"
        res = self.db.get(sql,email)
        if res:
            return res
        return None

    def register(self, nickname, email, password):
        if not self.check_email_is_not_exists(email):
            #TODO return
            return None
        ts = int(time.time())
        db_password = encrypt_password(password,str(ts))
        sql = "insert into user(nickname,email,password) values (%s,%s,%s);"
        try:
            user_id = self.db.execute_lastrowid(sql,nickname,email,db_password)
            return user_id
        except Exception,e:
            return None
        
    def login(self, email, password):
        res = self.get_ts_by_email(email)
        if not res:
            return None
        ts,user_id = res['ts'],res['id']
        db_password = encrypt_password(password,str(ts))
        if password<>db_password:
            return user_id
        return None

class FeedModel(BaseModel):

    def add(self):
        pass

    def delete(self):
        pass

class RelationModel(BaseModel):

    def is_follow(self):
        pass

    def add_follow(self):
        pass

    def remove_follow(self):
        pass

def main():
    user = UserModel()
    res = user.register('哈哈','ericsu1988@gmail.com','123456')
    print res

if __name__ == "__main__":
    main()
