#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
from handlers import BaseHandler


class ProfileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        user = self.get_current_user()
        current_user_id = user['id']
        notes = self.service.user_notes(user_id)
        self.render("profile.html",owner=self.service.get_user(user_id,current_user_id),notes=notes)
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        pass

class FriendHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        users = self.service.get_friends(user_id)
        self.render("friend.html",owner=self.service.get_user(user_id),users=users)

class FansHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        users = self.service.get_fans(user_id)
        self.render("fans.html",owner=self.service.get_user(user_id),users=users)

class TestHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("test.html")

routes = [
	(r'/([^/]+)/profile',ProfileHandler),
    (r'/([^/]+)/follow',FriendHandler),
    (r'/([^/]+)/fans',FansHandler),
    (r'/test',TestHandler)
]