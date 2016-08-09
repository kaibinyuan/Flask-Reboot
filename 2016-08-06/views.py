#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-02 19:38:15
# @Author  : yang ke (jack_keyang@163.com)

from run import app
from flask import redirect,request,render_template
from api import userinfo,checkinfo,adduser,deluser

@app.route("/index")
def index():
    names = userinfo()
    print names
    return render_template("index.html",nameinfo=names)

@app.route("/adduser")
def add_user():
    name = request.args.get("username")
    passwd =  request.args.get("password")
    if not checkinfo(name,passwd):
        return "user or password not null"
    if name in userinfo():
        return "user is exist"
    adduser(name,passwd)
    return redirect("/index")

@app.route("/deluser")
def del_user():
    name = request.args.get("username")
    if name in userinfo():
        deluser(name)
        return redirect("/index")
    else:
        return "username not found"