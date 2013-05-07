#!/usr/bin/env python
#-*-encoding:utf-8-*-

from handlers import BaseHandler
import tornado.web
import tornado.gen
import tornado.escape
from tornado import httpclient

class PhotoHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self,*args,**kwargs):
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch("https://api.weibo.com/2/statuses/public_timeline.json?source=720228000&count=60",
            callback=(yield tornado.gen.Callback("statuses")))
        response = yield tornado.gen.Wait("statuses")
        if response.error:
            print response
            self.set_header("Content-Type", "application/json")
            self.write(tornado.escape.json_encode({'is_success':False}))
            self.finish()
        else:
            res = tornado.escape.json_decode(response.body)
            self.render("photo.html",statuses=res['statuses'],user = self.get_current_user())
            
routes = [
	(r'/([^/]+)/photo',PhotoHandler),
]