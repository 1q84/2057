#!/usr/bin/env python
#-*-encoding:utf-8-*-

from model import UserModel,NoteModel,CommentModel
user=UserModel()
note=NoteModel()
comment=CommentModel()

class Service:

    def __init__(self):
        pass

    def get_user(self, user_id):
        if not user_id:
            return
        return user.get(user_id)

    def batch_get_user(self,user_ids):
        if not user_ids:
            return
        return user.batch_get(user_ids)

    def register(self, nickname, email, password):
        if not nickname or not email or not password:
            #TODO 用户名、密码、昵称均不能为空
            return 
        user_id = user.register(nickname,email,password)
        if not user_id:
            return
        return user_id

    def login(self, email, password):
        if not email or not password:
            #TODO 用户名、密码不能为空
            return 
        user_id = user.login(email,password)
        if not user_id:
            return
        return user_id

    def create_note(self,title,content,author_id):
        if not title or not content or not author_id:
            return
        return note.create(title,content,author_id)

    def get_note(self,note_id):
        if not note_id:
            return
        return note.get(note_id)

    def batch_get_note(self,author_id):
        if not author_id:
            return
        return note.batch_get(author_id)

    def create_comment(self, note_id, user_id, content):

        if not note_id or not user_id or not content:
            return
        comment.create(note_id,user_id,content)

    def get_comment(self, comment_id):

        if not comment_id:
            return
        return comment.get(comment_id)

    def batch_get_comment(self, note_id):

        if not note_id:
            return
        return comment.batch_get(note_id)


def main():
    service = Service()
    user_id = service.login('ericsu1988@gmail.com','123456')
    print user_id

if __name__ == "__main__":
    main()