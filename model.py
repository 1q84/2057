#!/usr/bin/env python
#-*-encoding:utf-8-*-

import time
import string
from util import encrypt_password
from tornado.options import define, options
from tornado.database import Connection,IntegrityError

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
        return None

    def register(self, nickname, email, password):
        if not self.check_email_is_not_exists(email):
            #TODO return
            return None
        ts = int(time.time())
        db_password = encrypt_password(password,str(ts))
        sql = "insert into users(nickname,email,password) values (%s,%s,%s);"
        try:
            user_id = self.db.execute_lastrowid(sql,nickname,email,db_password)
            return user_id
        except Exception,e:
            return None
        
    def login(self, email, password):
        res = self.get_ts_by_email(email)
        if not res:
            return None
        ts,user_id,db_password = res['ts'],res['id'],res['password']
        password = encrypt_password(password,str(ts))
        if password == db_password:
            return user_id
        return None

class FeedModel(BaseModel):

    def create(self,title,content,author_id):
        slug_base = title.replace(" ", "-").lower()
        valid_letters = string.ascii_letters + string.digits + "-"
        slug_base = "".join(c for c in slug_base if c in valid_letters)[:90]
        tries = 0
        while True:
            try:
                slug = slug_base + "-" + str(tries) if tries > 0 else slug_base
                sql = "INSERT INTO feeds (title,slug,author_id,content,created) VALUES (%s,%s,%s,%s,DATE_ADD( UTC_TIMESTAMP( ) , INTERVAL 8 HOUR ))"
                return self.db.execute(sql, title, slug,author_id, content)
            except IntegrityError:
                tries += 1

    def update(self):
        pass

    def delete(self):
        pass

    def get(self,author_id):
        sql = "SELECT * from feeds where author_id = %s order by id desc;"
        res = self.db.query(sql,author_id)
        return res

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
