#!/usr/bin/env python
#coding=utf8

from tornado.web import RequestHandler,HTTPError

class BaseHandler(RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user_id")

class ErrorHandler(BaseHandler):
    def prepare(self):
        super(ErrorHandler, self).prepare()
        self.set_status(404)
        raise HTTPError(404)