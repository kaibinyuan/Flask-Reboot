#!/usr/bin/env python
#coding:utf-8
from flask import Flask,request,render_template,redirect,session
import json 
from db import *

app = Flask(__name__)
app.secret_key="abcdefg"

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        login_info = dict((k,v[0]) for k,v in dict(request.form).items())
        if not checkuser({"name":login_info["name"]},"name"):
            return json.dumps({"code":1,"errmsg":"user is not exist"})
        if login_info["password"] != checkuser({'name':login_info["name"]})[0]:
            return json.dumps({"code":1,"errmsg":"password error"})
        else:
            u_role = checkuser({"name":login_info["name"]},"role")
            session["username"] = login_info["name"]
            session["role"] = u_role
            return json.dumps({"code":0,"result":"Login Successful"})

@app.route('/')
@app.route('/index')
def index():
    if not session.get('username',None):
	return redirect("/login")
    return  render_template('index.html')

@app.route('/logout/')
def logout():
    if session.get('username'):
	session.pop('role',None)
	session.pop('username',None)
    return redirect("/login")

@app.route("/userlist/")
def user_list():
    if not session.get('username',None):
	return redirect("/login")
    fields = ["id","name","name_cn","mobile","email","role","status"]
    data = userlist(fields)
    return render_template("userlist.html",users = data,info=session)

@app.route("/add",methods=["GET","POST"])
def add_user():
    if not session.get('username',None):
	return redirect("/login")
    if request.method == "GET":
        return render_template("add.html",info=session)
    if request.method == "POST":
         data = dict((k,v[0]) for k,v in dict(request.form).items())
         if data["name"] in checkuser({"name":data["name"]},"name"):
            return json.dumps({"code":1,"errmsg":"Username is exist"})
         adduser(data)
         return json.dumps({"code":0,"result":"Add User Successful"})

@app.route("/delete",methods=["GET"])
def del_user():
    if not session.get('username',None):
        return redirect("/login")
    uid = request.args.get('id',None)
    print uid
    delete(uid)
    return json.dumps({"code":0,"result":"Delete User Successful"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090,debug=True)
