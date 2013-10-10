#!/usr/bin/env python
#-*-encoding:utf-8-*-
from handlers import BaseHandler
import tornado.web
from utils import mark_down

class NoteHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self, note_id):
        if not note_id:
            note_id = self.get_argument('note_id', None)
        note = self.service.get_note(note_id)
        owner = self.service.get_user(note['author_id'],self.get_current_user().get('id'))
        note.update({'user':owner})
        comments = self.service.batch_get_comment(note_id)
        if not note:
            return
        self.render("note.html",note=note,show_comments=comments,create_comment=True,flag=False,owner=owner)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):

        note_id = self.get_argument('note_id', None)
        user_id = self.get_argument('user_id',None)
        note_user_id = self.get_argument('note_user_id',None)
        if not user_id:
            user_id = self.get_current_user().get('id')
        content = self.get_argument('content',None)
        self.service.create_comment(note_id,note_user_id,user_id,content)
        self.redirect('/note/%s'%note_id)
        return
    
class CreateFeedHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("create.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        text = self.get_argument('content', None)
        if not title or not text:
            self.get()
        content = mark_down(text)
        author_id = self.get_argument('author_id', None)
        if not author_id:
            current_user = self.get_current_user()
            author_id=current_user['id']
        note_id = self.service.create_note(title,content,author_id)
        if not note_id:
            return 
        self.redirect('/note/%s'%note_id)
        return 

routes = [
    (r"/create",CreateFeedHandler),
    (r"/note/([^/]+)",NoteHandler),
]