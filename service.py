#!/usr/bin/env python
#-*-encoding:utf-8-*-

from model import UserModel
user=UserModel()

class Service:

    def __init__(self):
        self.user = user

    def register(self, nickname, email, password):
        user_id = user.register(nickname,email,password)
        if not user_id:
            return
        return user_id

    def login(self, email, password):
        user_id = user.login(email,password)
        if not user_id:
            return 
        return user_id

def main():
    service = Service()
    user_id = service.login('ericsu1988@gmail.com','123456')
    print user_id

if __name__ == "__main__":
    main()