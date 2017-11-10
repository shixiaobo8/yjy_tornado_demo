#!/usr/bin/env python
# -*- coding:utf8 -*-
# __author:bobo
import tornado.ioloop
import tornado.web
import os,stat
import tornado.autoreload
import hashlib
import json


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        url = self.get_login_url()
        username = self.get_argument("username")
        password = self.get_argument("password")
        data = dict()
        if username == 'admin' and password=='wuyingbo56':
            with open('/root/filed.json') as f:
                # data = eval(f.readlines()[0])
                data = f.readlines()
            # data_k = data.keys()
            # data_v = data.values()
            self.render('inter_center_new.html',data=data)
        else:
            self.write("用户名或密码不正确")


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        list = [1,2,3,4,5]
        dict= {"code":200,"data":"ok"}
        self.render("login.html",dict=dict,list=list)

    def post(self, *args, **kwargs):
        self.write('aaaa')


class gameIntersHandler (tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
            signature = self.get_argument('signature',default=None)
            timestamp = self.get_argument('timestamp',default=None)
            nonce = self.get_argument('nonce',default=None)
            echostr = self.get_argument('echostr',default=None)
            token = "weixin_devops89" #请按照公众平台官网\基本配置中信息填写
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                self.write(echostr)
            else:
                self.write("")


class tableTestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
            with open('/root/filed.json') as f:
                data = f.readlines()
            res = dict()
            temp = []
            for d in data:
                temp.append(eval(d))
            res['rows'] = temp
            res['total'] = len(list(data))
            self.write(res)


class interFeildDeleteHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            key = self.get_argument('key',default=None)
            if key:
                self.write(key)



class interFeildSaveHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            key = self.get_argument('key',default=None)
            if key:
                self.write(key)


class interFeildAddHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            key = self.get_argument('key',default=None)
            if key:
                self.write(key)



class wxTokenHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            signature = self.get_argument('signature',default=None)
            timestamp = self.get_argument('timestamp',default=None)
            nonce = self.get_argument('nonce',default=None)
            echostr = self.get_argument('echostr',default=None)
            token = "weixin_devops89" #请按照公众平台官网\基本配置中信息填写
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                self.write(echostr)
            else:
                self.write("")


settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    # "xsrf_cookies": True,
    "debug":True
}
application = tornado.web.Application(
    handlers=[(r"/",MainHandler),
     (r"/wxauth",wxTokenHandler),
     (r"/inter_center",gameIntersHandler),
    (r"/tabletest",tableTestHandler),
    (r"/interFeildDelete",interFeildDeleteHandler),
    (r"/interFeildSave",interFeildSaveHandler),
    (r"/interFeildAdd",interFeildAddHandler),
     (r"/login",LoginHandler)],
    default_host='localhost',
    template_path=os.path.join(os.path.dirname(__file__),"templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    static_url_prefix = "/s/",
    **settings
)


if __name__ == '__main__':
    application.listen("99")
    tornado.ioloop.IOLoop.instance().start()
