#!/usr/bin/env python
#-*-encoding:utf-8-*-

from model import UserModel,NoteModel,CommentModel,RelationModel,NotificationModel
from utils import NOTIFICATION

class Service(object):

    def __init__(self):
        self.user=UserModel.instance()
        self.note=NoteModel.instance()
        self.comment=CommentModel.instance()
        self.relation=RelationModel.instance()
        self.notification = NotificationModel.instance()

    @classmethod
    def instance(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = cls()
        return cls._instance

    def get_user(self, user_id, current_user_id=None):
        if not user_id:
            return
        user = self.user.get(user_id)
        #TODO add count
        count = self.get_user_count(user_id)
        user.update(count)
        user['avatar'] = 'http://127.0.0.1:8888/static/uploads/avatar/'+user['avatar']
        if long(user_id)!=current_user_id:
            relation_status = self.relation.get_relation_status(current_user_id,user_id)
            user.update(relation_status)
        return user

    def batch_get_user(self,user_ids):
        if not user_ids:
            return []
        return self.user.batch_get(user_ids)

    def register(self, nickname, email, password):
        if not nickname or not email or not password:
            #TODO 用户名、密码、昵称均不能为空
            return 
        user_id =self.user.register(nickname,email,password)
        if not user_id:
            return
        return user_id

    def login(self, email, password):
        if not email or not password:
            #TODO 用户名、密码不能为空
            return 
        user_id = self.user.login(email,password)
        if not user_id:
            return
        return user_id

    def update_user(self, user_id, nickname, gender, description, avatar):
        return self.user.update(user_id,nickname, gender, description, avatar)

    def create_note(self,title,content,author_id):
        if not title or not content or not author_id:
            return
        return self.note.create(title,content,author_id)

    def get_note(self,note_id):
        if not note_id:
            return
        return self.note.get(note_id)

    def batch_get_note(self,author_ids,page):
        if not author_ids:
            return
        return self.note.batch_get(author_ids,page)

    def create_comment(self, note_id, note_user_id, user_id, content):

        if not note_id or not user_id or not content:
            return
        self.comment.create(note_id,user_id,content)
        self.add_notification(user_id,note_user_id,content,NOTIFICATION.COMMENT,note_id)

    def get_comment(self, comment_id):

        if not comment_id:
            return
        return self.comment.get(comment_id)

    def batch_get_comment(self, note_id):

        if not note_id:
            return
        return self.comment.batch_get(note_id)

    def get_friend_ids(self, user_id):
        friend_ids = self.relation.get_friend_ids(user_id)
        return friend_ids

    def get_fans_ids(self, user_id):
        fans_ids = self.relation.get_fans_ids(user_id)
        return fans_ids

    def get_friends(self, user_id):
        friend_ids = self.get_friend_ids(user_id)
        users = self.batch_get_user(friend_ids)
        return users

    def get_fans(self, user_id):
        fans_ids = self.get_fans_ids(user_id)
        users = self.batch_get_user(fans_ids)
        return users

    def get_user_count(self, user_id):
        note_count = self.note.get_note_count(user_id)
        friend_count = self.relation.get_friend_count(user_id)
        fans_count = self.relation.get_fans_count(user_id)
        return {
            'note_count':note_count,
            'friend_count':friend_count,
            'fans_count':fans_count
        }

    def user_notes(self, user_id):
        return self.note.get_user_note(user_id)

    def recent_notes(self):
        return self.note.get_recent_notes()

    def get_notification(self, user_id):
        notifications = self.notification.get_notification(user_id)
        if not notifications:
            return None
        from_user_ids = [notification['from_user_id'] for notification in notifications]
        from_user_ids.append(user_id)
        users = self.batch_get_user(from_user_ids)
        for user in users:
            user['avatar'] = 'http://127.0.0.1:8888/static/uploads/avatar/' + user['avatar']
        user_map = dict((u['id'],u) for u in users)
        for notification in notifications:
            notification['from_user'] = user_map[notification['from_user_id']]
            notification['to_user'] = user_map[notification['to_user_id']]
        return notifications

    def add_notification(self, from_user_id, to_user_id, message, notify_type, note_id=None):
        return self.notification.add_notification(from_user_id,to_user_id,message,notify_type,note_id)

def main():
    service = Service()
    users = service.get_friends(4)
    print users

if __name__ == "__main__":
    main()