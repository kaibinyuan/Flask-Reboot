#!/usr/bin/env python
#coding:utf8
import pickle

#ADD
def Create(username,password):
#    users = {'pc':'123456','wd':'123','kk':'234'}
    users = {username:password}
#pickle模块是以二进制形式存储在文件中,故必须以二进制形式打开
    with open('user.txt','wb') as f:
#将字典写入文件
	pickle.dump(users,f)

#DELETE
def Delete(username):
    name = username
    content = {}
#导入字典的时候不能用wb模式
    with open('user.txt') as f:
#将文件导入到字典中
	content = pickle.load(f)
    	content.pop(name)
#修改后的字典再次写入文件,文件必须以二进制的形式打开
    with open('user.txt','wb') as f:
	pickle.dump(content,f)

#Modify
def Modify(username,password):
    name = username
    password = password
    content = {}
    with open('user.txt') as f:
	content = pickle.load(f)
	content[name]= password
    with open('user.txt','wb') as f:
	pickle.dump(content,f)

#Find All
def Select():
    content = {}
    with open('user.txt') as f:
	content = pickle.load(f)
    for k,v in content.items():
	print "用户信息: %s ---> %s" %(k,v)
    return content

#Find One
def SelectOne(username):
    name = username
    content = {}
    userinfo = {}
    with open('user.txt') as f:
	content = pickle.load(f)
    userinfo[name] = content[name]
    print userinfo
    return userinfo
    
Create('lalala','123456')
#Delete()
Modify('lalala','45678')
Select()
#SelectOne('pc')
