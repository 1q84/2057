#!/usr/bin/env python
#coding=utf8


from handlers import account,note,comment,home,user,notification
from handlers import ErrorHandler

routes = []
routes.extend(home.routes)
routes.extend(account.routes)
routes.extend(note.routes)
routes.extend(user.routes)
routes.extend(notification.routes)
routes.append((r"/(.*)", ErrorHandler))
