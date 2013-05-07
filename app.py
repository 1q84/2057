#-*-encoding:utf-8-*-
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

define("port", default=8888, help="run on the given port", type=int)
define('photo_save_path', default = 'static/uploads/', type = str, help = 'where to put user\'s photos')
define('avatar_save_path', default = 'static/uploads/avatar/', type = str, help = 'where to put avatar')
options.log_file_prefix = 'log/web.log'

class NoteModule(tornado.web.UIModule):
    def render(self, note, show_comments=False,create_comment=False,flag=True):
        return self.render_string("modules/note.html", note=note, show_comments=show_comments,
                                  create_comment=create_comment, flag=flag)
class CommentModule(tornado.web.UIModule):
    def render(self, comment):
        return self.render_string("modules/comment.html", comment=comment)

class UserModule(tornado.web.UIModule):
    def render(self, user):
        return self.render_string("modules/user.html", user=user)
        
class Application(tornado.web.Application):
    
    def __init__(self):
        from urls import routes as handlers
        settings = dict(
            blog_title=u"2057 文字站|给未来的你或是自己",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Note": NoteModule,"Comment":CommentModule,"User":UserModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/account/login",
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