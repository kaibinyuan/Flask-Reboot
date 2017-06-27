#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request,render_template,redirect,session
import json
import userDB
import hashlib
from web_portal import app

app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
salt = "123"

user_db = userDB.UserDB()


# 首页,个人中心
@app.route('/')
@app.route('/index')
def index():
    if not session.get('username', None):
        return redirect("/login")
    result = user_db.getone({'name': session['username']})
    print result
    # {'status': 0, 'name': u'tantianran', 'mobile': u'1355555555', 'name_cn': u'tantianran', 'id': 15L, 'role': u'CU', 'email': u'tantianran@reboot.com'}
    session["id"] = result['id']
    print session
    # <SecureCookieSession {u'username': u'tantianran', u'role': u'CU'}>
    return render_template('user/index.html', info=session, user=result)


# 用户列表
@app.route("/userlist/")
def user_list():
    if not session.get('username', None):
        return redirect("/login")
    fields = ["id", "name", "name_cn", "mobile", "email", "role", "status"]
    data = user_db.userlist(fields)
    return render_template("user/userlist.html", users=data, info=session)


# 添加用户
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if not session.get('username', None):
        return redirect("/login")
    if request.method == "GET":
        return render_template("user/add.html", info=session)
    if request.method == "POST":
        data = dict((k, v[0]) for k, v in dict(request.form).items())
        # Hash 加密 Password
        data['password'] = hashlib.md5(data['password']+salt).hexdigest()
        #if data["name"] in checkuser({"name":data["name"]},"name"):
        #   return json.dumps({"code":1,"errmsg":"Username is exist"})
        user_db.adduser(data)
        return json.dumps({"code": 0, "result": "Add User Successful"})


# 删除用户
@app.route("/delete", methods=["GET"])
def del_user():
    if not session.get('username', None):
        return redirect("/login")
    uid = request.args.get('id', None)
    print uid
    user_db.delete(uid)
    return json.dumps({"code": 0, "result": "Delete User Successful"})


# 更新用户
@app.route('/update', methods=["GET", "POST"])
def update():
    if request.method == "GET":
        uid = request.args.get("id")
        user_info = user_db.getone({"id": uid})
        print json.dumps(user_info)
        return json.dumps(user_info)
    else:
        user_info = dict((k, v[0]) for k, v in dict(request.form).items())
        # user_info = request.form
        print user_info
        user_db.modfiy(user_info)
        return json.dumps({"code": 0})
