#!/usr/bin/env python
#-*-encoding:utf-8-*-

from handlers import BaseHandler
import tornado.web

class HomeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        author_id = self.get_argument('author_id', None)
        page = self.get_argument('p', None)
        if not author_id:
            current_user = self.get_current_user()
            author_id=current_user['id']

        users = self.service.get_friends(author_id)
        for user in users:
            user['avatar'] = 'http://127.0.0.1:8888/static/uploads/avatar/' + user['avatar']
        users.append(self.get_current_user())
        user_ids = [u['id'] for u in users]
        user_ids = list(set(user_ids))
        notes = self.service.batch_get_note(user_ids,page)
        recent_notes = self.service.recent_notes()
        user_map = dict((str(u['id']),u) for u in users)
        for note in notes:
            note.update({'user':user_map['%s'%note['author_id']]})
        self.render("timeline.html",notes=notes,user=self.get_current_user(),recent_notes=recent_notes)

class NewHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        author_id = self.get_argument('author_id', None)
        page = self.get_argument('p', None)
        if not author_id:
            current_user = self.get_current_user()
            author_id=current_user['id']

        users = self.service.get_friends(author_id)
        for user in users:
            user['avatar'] = 'http://127.0.0.1:8888/static/uploads/avatar/' + user['avatar']
        users.append(self.get_current_user())
        user_ids = [u['id'] for u in users]
        user_ids = list(set(user_ids))
        notes = self.service.batch_get_note(user_ids,page)
        recent_notes = self.service.recent_notes()
        user_map = dict((str(u['id']),u) for u in users)
        for note in notes:
            note.update({'user':user_map['%s'%note['author_id']]})
        self.render("test.html",notes=notes,user=self.get_current_user(),recent_notes=recent_notes)

class DemoHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('demo.html')

routes = [
	(r'/',HomeHandler),
    (r'/new',NewHandler),
    (r'/demo',DemoHandler)
]