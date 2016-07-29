#!/usr/bin/env python
# coding:utf-8


#获取用户
def get_user():
    res = {}
    with open('/root/dbfile.txt') as db:
        for line in db:
            tmp = line.rstrip('\n').split(':')
            res[tmp[0]] = tmp[1]
    return res


#注册
def register():
    with open('/root/dbfile.txt', 'a+') as db:
        while True:
            username = raw_input("请输入用户名: ").strip()
            password = raw_input("请输入密码: ").strip()
            repass = raw_input("请再次输入密码: ").strip()
            if len(username) == 0:
                print "用户名不能为空,请重新输入!!!"
                continue
            elif username in get_user():
                print "该用户名已存在,请重新输入!!!"
		continue
            elif len(password) == 0 or password != repass:
                print "密码与上一次输入不一致!!!"
                continue
            else:
                print "恭喜你,注册成功!!!"
                break
        db.write("%s:%s\n" % (username, password))

#登录
def login():
    count = 0
    while True:
        count += 1
        if count > 3:
            print "对不起,你输入的错误次数过多,账户已经被锁定,请联系管理员!!!"
            break
        username = raw_input("请输入用户名: ").strip()
        if username not in res:
            print "用户名不存在,请重新输入"
            continue
        password = raw_input("请输入密码: ").strip()
        if password != res[username]:
            print "密码输入有误!!!"
            continue
        else:
            print "恭喜你,登录成功!!!"
            break

def start():
    while True:
        result = raw_input("1.登录\n2.注册\n3.退出\n\n\n").strip()
        res = get_user()
        if result == '1':
            login()
            break
        elif result == '2':
            register()
            break
        elif result == '3':
            break
        else:
            print "没有选择任何功能现在退出"
            break

if __name__ == '__main__':
    start()
