#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-02 20:21:54
# @Author  : yang ke (jack_keyang@163.com)

userfile = "user.txt"

def userinfo():
    dic = {}
    with open(userfile) as f:
        for line in f:
            tmp = line.strip().split(":")
            dic[tmp[0]] = tmp[1]
        return dic

def adduser(user,passwd):
    with open(userfile,"a+") as f:
        f.write("%s:%s\n"%(user,passwd))

def checkinfo(user,passwd):
    if len(user) != 0 or len(passwd) != 0:
        return True

def deluser(user):
    dic = userinfo()
    del dic[user]
    userstr = "\n".join(map(lambda x: ":".join(x),dic.items()))
    with open(userfile,"w+") as f:
        f.writelines("%s\n"%userstr)
