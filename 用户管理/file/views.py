#!/usr/bin/env python
# -*- coding: utf-8 -*-

from run import app
from flask import redirect,request,render_template
import user

filename = 'user.txt'
user = user.User(filename)
user.info()


@app.route("/index")
def index():
    names = user.info()
    print names
    return render_template("index.html", nameinfo=names)


@app.route("/adduser")
def add_user():
    username = request.args.get("username")
    password = request.args.get("password")

    if not user.check(username, password):
        return "user or password not null"

    if username in user.info():
        return "user is exist"

    user.add(username, password)
    return redirect("/index")


@app.route("/deluser")
def del_user():
    name = request.args.get("username")

    if name in user.info():
        user.delete(name)
        return redirect("/index")
    else:
        return "username not found"
