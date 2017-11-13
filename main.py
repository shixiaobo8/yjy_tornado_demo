#!/usr/bin/env python
# -*- coding:utf8 -*-
# __author:bobo
import tornado.ioloop
import tornado.web
import os,stat
import tornado.autoreload
import hashlib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        url = self.get_login_url()
        username = self.get_argument("username")
        password = self.get_argument("password")
        data = dict()
        if username == 'admin' and password=='wuyingbo56':
            with open(self.application.settings['field_files']) as f:
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


class getInterData():
    def getInterFeilds(self):
        res = dict()
        file = self.application.settings['field_files']
        with open(file) as f:
            data = f.readlines()
        for d in data:
            dkv = eval(d)
            res[dkv['key']] = dkv['value']
        return res


class intersMainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        it = getInterData()
        res = it.getInterFeilds()
        self.finish(res)
    def post(self, *args, **kwargs):
        it = getInterData()
        res = it.getInterFeilds()
        self.finish(res)

class ShareGameHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        it = getInterData()
        fields = it.getInterFeilds()
        roomid=self.get_argument('roomid','0')
        peoples=self.get_argument('peoples','0')
        status = 'ok'
        res = {"id": "penghu",
          'scheme_ios': "'yinjiapenghu://?mid=0&version="+fields['version']+"&roomid=" + roomid + "&peoples=" + peoples + "&amp;timestamp=' + Date.parse(new Date())",
          'scheme_android': "'yinjiapenghu://com.yinjia.penghu?mid=0&version="+fields['version']+"&roomid=" + roomid + "&peoples=" + peoples + "&amp;timestamp=' + Date.parse(new Date())",
          'ios_download': 'apk/YinJiaPengHu.apk',
          'android_download': 'apk/YinJiaPengHu.apk',
          'timeout': 1000};
        href = "yinjiapenghu://com.yinjia.penghu?mid=0&version="+fields['version']+"&roomid=" + roomid + "&peoples=" + peoples
        res1 = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <title>银佳碰胡加入房间</title>
            </head>
            <body>
                <style type="text/css">
                *{margin:0; padding:0;}
                img{max-width: 100%; height: auto;}
                .test{height: 600px; max-width: 600px; font-size: 18px;}
                </style>
            <div class="test">
                <center><h4>银佳碰胡——欢迎你 </h4></center><h4><center> 房间号: """ + roomid +  """</h4></center><h4><center> 当前人数: """ + peoples +  """</h4></center><center><h4 onclick='startAPP()' style="color:red;border 1px solid green;"><b style='font-size:100px;'><img src='http://www.devops89.cn:56/jionRoomBtn.png' alt='加入房间'/> </b></h4></center>
                <br/><center>没有安装请点击下面的按钮下载</center><br/>
                <center><input type='image' src='http://www.devops89.cn:56/downloadBtn.png' onclick='downLoadApp()' alt='点击下载app'/></center>
                </div>
                <script>
                                function downLoadApp(){
                                    window.open("http://www.devops89.cn:56/apk/YinJiaPengHu.apk");
                                };
                                function startAPP(){
                                    window.location = '"""+ href+"""';
                                    }
                                </script>

                <script type="text/javascript">
                    function is_weixin() {
                        var ua = navigator.userAgent.toLowerCase();
                        if (ua.match(/MicroMessenger/i) == "micromessenger") {
                            return true;
                        } else {
                            return false;
                        }
                    }
                    var isWeixin = is_weixin();
                    var winHeight = typeof window.innerHeight != 'undefined' ? window.innerHeight : document.documentElement.clientHeight;
                    function loadHtml(){
                        var div = document.createElement('div');
                        div.id = 'weixin-tip';
                        div.innerHTML = '<p><img src="http://www.devops89.cn:56/live_weixin.png" alt="微信打开"/></p>';
                        document.body.appendChild(div);
                    }

                    function loadStyleText(cssText) {
                        var style = document.createElement('style');
                        style.rel = 'stylesheet';
                        style.type = 'text/css';
                        try {
                            style.appendChild(document.createTextNode(cssText));
                        } catch (e) {
                            style.styleSheet.cssText = cssText; //ie9以下
                        }
                        var head=document.getElementsByTagName("head")[0]; //head标签之间加上style样式
                        head.appendChild(style);
                    }
                    var cssText = "#weixin-tip{position: fixed; left:0; top:0; background: rgba(0,0,0,0.8); filter:alpha(opacity=80); width: 100%; height:100%; z-index: 100;} #weixin-tip p{text-align: center; margin-top: 10%; padding:0 5%;}";
                    if(isWeixin){
                        loadHtml();
                        loadStyleText(cssText);
                    }
                </script>
            </body>
            </html>
            """
        self.write(res1)


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
            file = self.application.settings['field_files']
            with open(file) as f:
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
            value = self.get_argument('value',default=None)
            if key and value:
                delFiled = "{'key':'" + key + "','value':'" + value+"'}\n"
                data = ''
                with open(self.application.settings['field_files']) as f:
                    data = f.read()
                if delFiled not in data:
                    delFiled = delFiled.replace('\n','')
                data = data.replace(delFiled,'')
                with open(self.application.settings['field_files'],'w+') as f:
                    f.write(data)
                self.finish({'code':200,'data':'删除成功'})
            else:
                self.finish({'code':500,'data':'参数错误!'})


class interFeildSaveHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            key = self.get_argument('key',default=None)
            value = self.get_argument('value',default=None)
            if key and value:
                k_f = "'key':'" + key + "'"
                v_f = "'value':'" + value + "'"
                new_f = "{'key':'" + key + "','value':'" + value+"'}"
                with open(self.application.settings['field_files']) as f:
                    data = f.read()
                # 只修改value
                if k_f in ''.join(data) and v_f not in ''.join(data):
                    old_f = "{'key':'" + key + "'"
                    new_c = ''
                    for d in data.split('\n'):
                        if d.startswith(old_f):
                            new_c += new_f + '\n'
                        else:
                            new_c += d + '\n'
                    if new_c.endswith('\n'):
                        new_c = new_c[0:-1]
                    with open(self.application.settings['field_files'],'w+') as f:
                        f.write(new_c)
                    self.finish({'code':200,'data':new_c,'mess':'修改v成功'})
                # 只修改key
                elif v_f in ''.join(data) and k_f not in ''.join(data):
                    old_v = "'value':'" + value + "'}"
                    new_c = ''
                    for d in data.split('\n'):
                        if d.endswith(old_v):
                            new_c += new_f + '\n'
                        else:
                            new_c += d + '\n'
                    if new_c.endswith('\n'):
                        new_c = new_c[0:-1]
                    with open(self.application.settings['field_files'],'w+') as f:
                        f.write(new_c)
                    self.finish({'code':200,'data':new_c,'mess':'修改k成功'})
                # 修改key 和value
                elif v_f in ''.join(data) and k_f in ''.join(data):
                    self.finish({'code':200,'data':new_c,'mess':'kv未变化'})
                else:
                    self.finish({'code':202,'mess':'不支持的操作,kv错误'})
            else:
                self.finish({'code':500,'mess':'参数错误!'})


class interFeildAddHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
            key = self.get_argument('key',default=None)
            value = self.get_argument('value',default=None)
            if key and value:
                k_f = "'key':'" + key + "'"
                new_f = "{'key':'" + key + "','value':'" + value+"'}"
                with open(self.application.settings['field_files']) as f:
                    data = f.readlines()
                if k_f in ''.join(data):
                    self.finish({'code':202,'data':'对不起,已存在相同的字段和值'})
                else:
                    with open(self.application.settings['field_files'],'a+') as f:
                        f.write('\n')
                        f.write(new_f)
                    self.finish({'code':200,'data':data,'k':k_f})
            else:
                self.finish({'code':500,'data':'参数错误!'})



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
    (r"/logine",intersMainHandler),
    (r"/share.html",ShareGameHandler),
     (r"/login",LoginHandler)],
    default_host='localhost',
    template_path=os.path.join(os.path.dirname(__file__),"templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    field_files=os.path.join(os.path.dirname(__file__),'filed.json'),
    # field_files='/root/filed.json',
    static_url_prefix = "/s/",
    **settings
)


if __name__ == '__main__':
    application.listen("99")
    tornado.ioloop.IOLoop.instance().start()
