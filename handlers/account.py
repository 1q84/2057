#!/usr/bin/env python
#-*-coding:utf-8-*-

import tornado.web
import tornado.gen
from handlers import BaseHandler
import os.path, random, string
from tornado.options import define, options
import logging
import utils

class RegisterHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.render("register.html")

    def post(self, *args, **kwargs):
        nickname = self.get_argument("nickname", None)
        email = self.get_argument("email", None)
        password = self.get_argument("password",None)
        user_id = self.service.register(nickname,email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return
        self.get()

class LoginHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        user_id = self.service.login(email,password)
        if user_id:
            self.set_secure_cookie('user_id',str(user_id))
            self.redirect("/")
            return
        self.get()

class LogoutHandler(BaseHandler):

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect('/account/login')
        return

class SettingsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("setting.html")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user = self.get_current_user()
        user_id = user['id']
        nickname = self.get_argument("nickname", None)
        gender = self.get_argument("gender", 0)
        description = self.get_argument("description", None)
        avatar_id = 'default'
        if self.request.files.has_key('fileupload'):
            file_upload = self.request.files['fileupload'][0]
            original_filename = file_upload['filename']
            extension = os.path.splitext(original_filename)[1]
            avatar_image_buffer = file_upload['body']
            avatar_id = self.write_and_upload_file(user_id,extension,avatar_image_buffer)
        self.service.update_user(user_id,nickname,gender,description,avatar_id)
        self.redirect('/account/settings')
        return
    
    def write_and_upload_file(self,user_id,extension,file_buffer):
        filename = utils.gen_avatar_path() + extension
        tmp_file = open(options.avatar_save_path + filename, 'wb')
        tmp_file.write(file_buffer)
        tmp_file.close()
        return filename

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file_upload = self.request.files['fileupload'][0]
        original_filename = file_upload['filename']
        extension = os.path.splitext(original_filename)[1]
        filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= filename+extension
        output_file = open(options.photo_save_path + final_filename, 'w')
        output_file.write(file_upload['body'])
        logging.debug("file" + final_filename + " is uploaded")
        self.redirect("/account/settings")
        return 
           
routes = [
	(r'/account/login/*',LoginHandler),
	(r'/account/logout/*',LogoutHandler),
    (r'/account/register/*',RegisterHandler),
    (r'/account/settings',SettingsHandler),
    (r'/account/index',IndexHandler),
    (r'/account/upload',UploadHandler)
]