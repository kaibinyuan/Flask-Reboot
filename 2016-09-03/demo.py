#!/usr/bin/env python
#coding:utf-8
from flask import Flask,request,render_template,redirect,session
import json 
from db import *
import hashlib

app = Flask(__name__)
app.secret_key="abcdefg"
salt = "123"
#登录
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        login_info = dict((k,v[0]) for k,v in dict(request.form).items())
	#Password 加密回去对照数据库
	login_info['password'] = hashlib.md5( login_info['password'] + salt).hexdigest()
	print login_info  #{'password': u'123456', 'name': u'yuanbinbin'}
	fields = ['name','password','role','status']
	result = checkuser({"name":login_info["name"]},fields)
	print result   #{'status': 0, 'password': u'123456', 'role': u'admin', 'name': u'yuanbinbin'}
	if not result:
            return json.dumps({"code":1,"errmsg":"user is not exist"})
        if login_info["password"] != result['password']:
            return json.dumps({"code":1,"errmsg":"password error"})
	if int(result['status']) == 1:
	    return json.dumps({"code":1,"errmsg":"账户被锁定"})
        session["username"] = login_info["name"]
        session["role"] = result['role']
        return json.dumps({"code":0,"result":"Login Successful"})

#首页,个人中心
@app.route('/')
@app.route('/index')
def index():
    if not session.get('username',None):
	return redirect("/login")
    result = getone({'name':session['username']})
    print result
    #{'status': 0, 'name': u'tantianran', 'mobile': u'1355555555', 'name_cn': u'tantianran', 'id': 15L, 'role': u'CU', 'email': u'tantianran@reboot.com'}
    print session
    #<SecureCookieSession {u'username': u'tantianran', u'role': u'CU'}>
    return  render_template('index.html',info=session,user=result)

#退出
@app.route('/logout/')
def logout():
    if session.get('username'):
	session.pop('role',None)
	session.pop('username',None)
    return redirect("/login")

#用户列表
@app.route("/userlist/")
def user_list():
    if not session.get('username',None):
	return redirect("/login")
    fields = ["id","name","name_cn","mobile","email","role","status"]
    data = userlist(fields)
    return render_template("userlist.html",users = data,info=session)

#添加用户
@app.route("/add",methods=["GET","POST"])
def add_user():
    if not session.get('username',None):
	return redirect("/login")
    if request.method == "GET":
        return render_template("add.html",info=session)
    if request.method == "POST":
         data = dict((k,v[0]) for k,v in dict(request.form).items())
	 #Hash 加密 Password
	 data['password'] = hashlib.md5(data['password']+salt).hexdigest()
         #if data["name"] in checkuser({"name":data["name"]},"name"):
         #   return json.dumps({"code":1,"errmsg":"Username is exist"})
         adduser(data)
         return json.dumps({"code":0,"result":"Add User Successful"})

#删除用户
@app.route("/delete",methods=["GET"])
def del_user():
    if not session.get('username',None):
        return redirect("/login")
    uid = request.args.get('id',None)
    print uid
    delete(uid)
    return json.dumps({"code":0,"result":"Delete User Successful"})

#更新用户
@app.route('/update',methods=["GET","POST"])
def update():
    if request.method == "GET":
        uid = request.args.get("id")
        userinfo = getone({"id":uid})
        print json.dumps(userinfo)
        return json.dumps(userinfo)
    else:
        userinfo = dict((k,v[0]) for k,v in dict(request.form).items())
	#userinfo = request.form
	print userinfo
        modfiy(userinfo)
        return json.dumps({"code":0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090,debug=True)
