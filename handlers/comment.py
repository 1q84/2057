#!/usr/bin/env python
#-*-encoding:utf-8-*-
from handlers import BaseHandler
from service import Service
import tornado.web
service=Service()

class CommentHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self, comment_id):

        if not comment_id:
            comment_id = self.get_argument('comment_id', None)
        comment = service.get_comment(comment_id)
        if not comment:
            return
        self.render("comment.html",comment=comment)