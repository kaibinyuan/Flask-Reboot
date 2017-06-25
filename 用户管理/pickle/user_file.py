#!/usr/bin/env python
# -*- coding:utf8 -*-
import pickle

class User:
    def __init__(self):
        pass

    @staticmethod
    def add(username, password):
        # users = {'pc':'123456','wd':'123','kk':'234'}
        user_info = {username:password}
        # pickle模块是以二进制形式存储在文件中,故必须以二进制形式打开
        with open('user.txt','wb') as f:
        # 将字典写入文件
        pickle.dump(user_info, f)

#DELETE
    @staticmethod
    def delete(username):
        name = username
        # 导入字典的时候不能用wb模式
        with open('user.txt') as f:
        # 将文件导入到字典中
	        content = pickle.load(f)
            content.pop(name)
        # 修改后的字典再次写入文件,文件必须以二进制的形式打开
        with open('user.txt','wb') as f:
            pickle.dump(content,f)

#Modify
    @staticmethod
    def modify(username,password):
        name = username
        password = password
        with open('user.txt') as f:
            content = pickle.load(f)
            content[name]= password
        with open('user.txt', 'wb') as f:
            pickle.dump(content, f)

# Show All
    @staticmethod
    def all():
        with open('user.txt') as f:
            content = pickle.load(f)

        for k,v in content.items():
            print "用户信息: %s ---> %s" %(k,v)
        return content

#Find One
    @staticmethod
    def info(username):
        name = username
        user_info = {}
        with open('user.txt') as f:
            content = pickle.load(f)
            user_info[name] = content[name]
        print user_info
        return user_info


if __name__ == '__main__':
    user = User()
    user.add('yuanbinbin', '123456')
