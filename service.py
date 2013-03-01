#!/usr/bin/env python
#-*-encoding:utf-8-*-

from model import UserModel,FeedModel
user=UserModel()
feed=FeedModel()

class Service:

    def __init__(self):
        self.user = user

    def register(self, nickname, email, password):
        if not nickname or not email or not password:
            #TODO 用户名、密码、昵称均不能为空
            return 
        user_id = user.register(nickname,email,password)
        if not user_id:
            return
        return user_id

    def login(self, email, password):
        if not email or not password:
            #TODO 用户名、密码不能为空
            return 
        user_id = user.login(email,password)
        if not user_id:
            return
        return user_id

    def create_feed(self,title,content,author_id):
        if not title or not content or not author_id:
            return
        feed.create(title,content,author_id)

    def get_feed(self,author_id):
        if not author_id:
            return
        return feed.get(author_id)

def main():
    service = Service()
    user_id = service.login('ericsu1988@gmail.com','123456')
    print user_id

if __name__ == "__main__":
    main()