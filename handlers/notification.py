#!/usr/bin/env python
#-*-coding:utf-8-*-

from handlers import BaseHandler
import tornado

class NotificationHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.get_current_user().get('id')
        notifications = self.service.get_notification(user_id)
        self.render("notification.html",notifications=notifications)

routes = [
    (r'/notification',NotificationHandler)
]