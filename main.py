#!/usr/bin/env python
# -*- coding:utf8 -*-
# __author:bobo
import tornado.ioloop
import tornado.web
import os,stat
import tornado.autoreload

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        url = self.get_login_url()
        list = [1,2,3,4,5]
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            os.chmod(upload_path,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
        username = self.get_argument("username")
        password = self.get_argument("password")
        files = self.request.files['file']
        file_name = ''
        upload_status = 0
        for f in files:
            file_name = f['filename']
            upload_status = self.save_file(f['body'],upload_path)
        res = {
                "code":200,
                'data': {
                    "username":username,
                    "password":password,
                    "文件名:":file_name,
                    "文件上传状态:":upload_status,
                    "request_url":url,
                    "参数0":list
                }
        }
        self.write(res)

    def save_file(self,file_contents,upload_path):
        status = 1
        with open(upload_path,"wb") as f:
            f.write(file_contents)
        return status

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        list = [1,2,3,4,5]
        dict= {"code":200,"data":"ok"}
        self.render("login.html",dict=dict,list=list)

    def post(self, *args, **kwargs):
        self.write('aaaa')

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    # "xsrf_cookies": True,
    "debug":True
}
application = tornado.web.Application(
    handlers=[(r"/",MainHandler),
     (r"/login",LoginHandler)],
    default_host='localhost',
    template_path=os.path.join(os.path.dirname(__file__),"templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    static_url_prefix = "/s/",
    **settings
)


if __name__ == '__main__':
    application.listen("80")
    tornado.ioloop.IOLoop.instance().start()
