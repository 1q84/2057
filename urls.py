#!/usr/bin/env python
#coding=utf8


from handlers import account,note,comment,home
from handlers import ErrorHandler

routes = []
routes.extend(home.routes)
routes.extend(account.routes)
routes.extend(note.routes)
routes.append((r"/(.*)", ErrorHandler))
