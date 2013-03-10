#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.gen
from handlers import BaseHandler

class RegisterHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.render("register.html")

    def post(self, *args, **kwargs):
        nickname = self.get_argument("nickname", None)
        email = self.get_argument("email", None)
        password = self.get_argument("password",None)
        user_id = self.service.register(nickname,email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return
        self.get()

class LoginHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user_id = self.service.login(email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return
        self.get()

class LogoutHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect('/account/login')
        return
    
routes = [
	(r'/account/login/*',LoginHandler),
	(r'/account/logout/*',LogoutHandler),
    (r'/account/register/*',RegisterHandler),
]