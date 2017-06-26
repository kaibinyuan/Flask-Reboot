#!/usr/bin/env python
# -*- coding:utf8 -*-
import pickle


class User:
    def __init__(self, filename):
        self.filename = filename

    def create(self, username, password):
        # users = {'pc':'123456','wd':'123','kk':'234'}
        user_info = {username: password}
        # pickle模块是以二进制形式存储在文件中,故必须以二进制形式打开
        with open(self.filename, 'wb') as f:
            # 将字典写入文件
            pickle.dump(user_info, f)

# DELETE
    def delete(self, username):
        name = username
        # 导入字典的时候不能用wb模式
        with open(self.filename) as f:
            # 将文件导入到字典中
            content = pickle.load(f)
            content.pop(name)
        # 修改后的字典再次写入文件,文件必须以二进制的形式打开
        with open(self.filename, 'wb') as f:
            pickle.dump(content, f)

# Modify
    def modify(self, username, password):
        name = username
        password = password
        with open(self.filename) as f:
            content = pickle.load(f)
            content[name] = password
        with open(self.filename, 'wb') as f:
            pickle.dump(content, f)

# Show All
    def all(self):
        with open(self.filename) as f:
            content = pickle.load(f)

        for k, v in content.items():
            print "用户信息: %s ---> %s" % (k, v)
        return content

# Find One
    def info(self, username):
        name = username
        user_info = {}
        with open(self.filename) as f:
            content = pickle.load(f)
            user_info[name] = content[name]
        print user_info
        return user_info


if __name__ == '__main__':
    filename = 'user.txt'
    user = User(filename)
    user.modify('shaojiabin', '123456')
    user.modify('nijing', '45678')
    user.delete('yuanbinbin')
    user.all()
