#!/usr/bin/env python
#coding=utf8

from tornado.web import RequestHandler,HTTPError
from service import Service

class BaseHandler(RequestHandler):

    @property
    def service(self):
        return Service.instance()

    def get_current_user(self):
        user_id=self.get_secure_cookie("user_id")
        return self.service.get_user(user_id) if user_id else None

class ErrorHandler(BaseHandler):
    def prepare(self):
        super(ErrorHandler, self).prepare()
        self.set_status(404)
        raise HTTPError(404)