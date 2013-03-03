#!/usr/bin/env python
#-*-encoding:utf-8-*-
from handlers import BaseHandler
from service import Service
import tornado.web
import markdown
service=Service()

class NoteHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self, note_id):

        if not note_id:
            note_id = self.get_argument('note_id', None)
        note = service.get_note(note_id)
        comments = service.batch_get_comment(note_id)
        if not note:
            return
        self.render("note.html",note=note,show_comments=comments,create_comment=True,flag=False)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):

        note_id = self.get_argument('note_id', None)
        user_id = self.get_argument('user_id',None)
        if not user_id:
            user_id = self.get_current_user()
        content = self.get_argument('content',None)
        service.create_comment(note_id,user_id,content)
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
        content = markdown.markdown(text)
        author_id = self.get_argument('author_id', None)
        if not author_id:
            author_id = self.get_current_user()
        note_id = service.create_note(title,content,author_id)
        if not note_id:
            return 
        self.redirect('/note/%s'%note_id)
        return 

routes = [
    (r"/create",CreateFeedHandler),
    (r"/note/([^/]+)",NoteHandler),
]