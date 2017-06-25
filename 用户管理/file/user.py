#!/usr/bin/env python
# -*- coding: utf-8 -*-


class User:
    def __init__(self, filename):
        self.filename = filename

    def info(self):
        dic = {}
        with open(self.filename) as f:
            for line in f:
                tmp = line.strip().split(":")
                dic[tmp[0]] = tmp[1]
        # dict: {'yuanbinbin': 'mofanghr', 'yang': '123', 'jack': '123', 'pangyantao': 'mfzp123456'}
        return dic

    def add(self, username, password):
        with open(self.filename, "a+") as f:
            f.write("%s:%s\n" % (username, password))

    @staticmethod
    def check(username, password):
        if len(username) != 0 or len(password) != 0:
            return True

    def delete(self, username):
        dic = self.info()
        del dic[username]
        # user_info:  yuanbinbin:mofanghr
        user_info = "\n".join(map(lambda x: ":".join(x), dic.items()))
        with open(self.filename, "w+") as f:
            f.writelines("%s\n" % user_info)

if __name__ == '__main__':
    filename = 'user.txt'
    user = User(filename)
    user.info()
    # user.add("pangyantao", 'mfzp123456')
    # user.info()
    user.delete('pangyantao')
    user.info()
