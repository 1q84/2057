import os
import tornado.ioloop
import tornado.web
import tornado.database
import tornado.options
import tornado.httpserver
from tornado.options import define,options
import tornado.autoreload
import time

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):

    pass

class HomeHandler(BaseHandler):
    
    def get(self, *args, **kwargs):
        self.render("timeline.html")

    def post(self, *args, **kwargs):
        self.render("timeline.html")

class RegisterHandler(BaseHandler):
    
    def get(self, *args, **kwargs):
        self.render("register.html")

    def post(self, *args, **kwargs):
        pass

class LoginHandler(BaseHandler):
    
    def get(self, *args, **kwargs):
        self.render("login.html")
        
    def post(self, *args, **kwargs):
        pass

class ProfileHandler(BaseHandler):
    
    def get(self, user_id):
        pass
        
class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/user/([^/]+)", ProfileHandler),
            (r"/register", RegisterHandler),
            (r"/login",LoginHandler)
        ]
        settings = dict(
            blog_title=u"2057",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
#            ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            autoescape=None,
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    ts = time.strftime('%Y%m%d',time.localtime(time.time()))
    log_path='server.%s.log'%ts
    options['log_file_prefix'].set(log_path)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    loop=tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
    
if __name__ == "__main__":
    main()