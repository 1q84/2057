#!/usr/bin/env python
#-*-encoding:utf-8-*-

from handlers import BaseHandler
from service import Service
import tornado.web
service=Service()

class HomeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        author_id = self.get_argument('author_id', None)
        if not author_id:
            author_id = self.get_current_user()
        notes = service.batch_get_note(author_id)
        user_ids = [note['author_id'] for note in notes]
        user_ids = list(set(user_ids))
        users = service.batch_get_user(user_ids)
        user_map = dict((str(u['id']),u) for u in users)
        for note in notes:
            note['user']=user_map['%s'%note['author_id']]
        self.render("timeline.html",notes=notes)

routes = [
	(r'/',HomeHandler),
]