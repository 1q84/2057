import os
import time
import logging
import tornado.ioloop
import tornado.web
import tornado.database
import tornado.options
import tornado.httpserver
from tornado.options import define,options
import tornado.autoreload
from service import Service
service = Service()

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user_id")
    
class HomeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("timeline.html")

class RegisterHandler(BaseHandler):
    
    def get(self, *args, **kwargs):
        self.render("register.html")

    def post(self, *args, **kwargs):
        nickname = self.get_argument("nickname", None)
        email = self.get_argument("email", None)
        password = self.get_argument("password",None)
        user_id = service.register(nickname,email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return
        self.get()

class LoginHandler(BaseHandler):
    
    def get(self, *args, **kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user_id = service.login(email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return 
        self.get()

class LogoutHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect('/login')
        return

class FeedHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        author_id = self.get_argument('author_id', None)
        if not author_id:
            author_id = self.get_current_user()
        feeds = service.get_feed(author_id)
        self.render("feed.html",feeds=feeds)

class CreateFeedHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("create.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        author_id = self.get_argument('author_id', None)
        if not author_id:
            author_id = self.get_current_user()
        service.create_feed(title,content,author_id)
        self.redirect('/feed')
        return 
            
class ProfileHandler(BaseHandler):
    
    def get(self, user_id):
        pass
        
class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/user/([^/]+)", ProfileHandler),
            (r"/register", RegisterHandler),
            (r"/login",LoginHandler),
            (r"/logout",LogoutHandler),
            (r"/feed",FeedHandler),
            (r"/feed/create",CreateFeedHandler),
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