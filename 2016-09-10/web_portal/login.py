#!/usr/bin/env python
#coding:utf-8
from flask import request,render_template,redirect,session
import json 
from db import *
import hashlib
from web_portal import app

app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
salt = "123"

#登录
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")
    if request.method == "POST":
        login_info = dict((k,v[0]) for k,v in dict(request.form).items())
	#Password 加密回去对照数据库
	login_info['password'] = hashlib.md5( login_info['password'] + salt).hexdigest()
	print login_info  #{'password': u'123456', 'name': u'yuanbinbin'}
	fields = ['name','password','role','status']
	result = checkuser({"name":login_info["name"]},fields)
	print result    #{'status': 0, 'password': u'123456', 'role': u'admin', 'name': u'yuanbinbin'}
	if not result:
            return json.dumps({"code":1,"errmsg":"user is not exist"})
        if login_info["password"] != result['password']:
            return json.dumps({"code":1,"errmsg":"password error"})
	if int(result['status']) == 1:
	    return json.dumps({"code":1,"errmsg":"账户被锁定"})
        session["username"] = login_info["name"]
        session["role"] = result['role']
        return json.dumps({"code":0,"result":"Login Successful"})

#退出
@app.route('/logout/')
def logout():
    if session.get('username'):
	session.pop('role',None)
	session.pop('username',None)
	session.pop('id',None)
    return redirect("/login")
