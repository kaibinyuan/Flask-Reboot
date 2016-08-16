#coding:utf-8

'''
	1.导入flask模块的(request,渲染模板,地址重写模块)
	2.导入python连接mysql模块
	3.导入json,time,traceback模块
'''
from flask import Flask,request,render_template,redirect
import MySQLdb as mysql
import json 
import time
import traceback

'''
	1.创建mysql连接
	2.设置sql语句自动提交
	3.设置游标
'''
conn=mysql.connect(user='root',host='127.0.0.1',passwd='123456',db='reboot',charset='utf8')
conn.autocommit(True) 
cur = conn.cursor()

#固定语法
app = Flask(__name__)

# 注册，即添加用户,第一次请求获取注册页面，用GET请求，点击表单按钮提交用post方式，执行sql插入数据，注册成功则跳转到个人信息页面，失败则在注册页面打印错误信息
#'/register' 路由允许get,post两种方式
@app.route('/register',methods=['GET','POST'])
def register():
#如果请求方式为'post'
    if request.method == 'POST':
#从html模板中获取用户信息,并保存在data字典中
        data =  {} 
        data["name"] = request.form.get('name',None)
        data["name_cn"] = request.form.get('name_cn',None)
        data["mobile"] = request.form.get('mobile',None)
        data["email"] = request.form.get('email',None)
        data["role"] = request.form.get('role',None)
        data["status"] = request.form.get('status',None)
        data["password"] = request.form.get('password',None)
        data["repwd"] = request.form.get('repwd',None)
        data["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # data = request.form
        # data = request.get_json()
        print data
#数据库操作
        fields = ['name','name_cn','mobile','email','role','status','password','create_time']
		#如果接收的'name','password','role'其中的一个为空则返回注册页面,并抛出异常'errmsg'
        if not data["name"] or not data["password"] or not data["role"]:
            errmsg = 'name or password or role not null'
            return render_template("register.html",result=errmsg)
        #如果接收的'password'和'repwd'不一致则返回注册页面,并抛出异常'errmsg'    
        if data["password"] != data["repwd"]:
            # return  json.dumps('code':1,'errmsg':'The two passwords you typed do not match.'
            errmsg = 'The two passwords you typed do not match'
            return render_template("register.html",result=errmsg)
		#将前端传递的数据写入数据库返回个人信息页面,如果不成功,则执行except语句
        try:
            sql = 'INSERT INTO users (%s) VALUES (%s)' % (','.join(fields), ','.join(['"%s"' % data[x] for x in fields]))
            cur.execute(sql)
            return redirect('/userinfo?name=%s' % data['name'])
		#写库失败,返回注册页面并抛出异常'errmsg'
        except:
            errmsg = "insert failed" 
            print traceback.print_exc()
            return render_template("register.html",result=errmsg)
#如果请求不为'post'
    else:
		#返回'register.html页面'
        return render_template("register.html")

# 用户列表，生产环境中只有管理员才有这个权限，暂时不设置权限
@app.route('/userlist')
def userlist():
#数据库操作
    users = []
    fields = ['id', 'name', 'name_cn', 'email', 'mobile']
	#尝试获取用户数据,并返回给前端一个字典类型数据'users',如果执行失败则执行'execpt'语句	
    try:
        sql = "select %s from users" % ','.join(fields) 	#sql语句
        cur.execute(sql)	#执行sql
        result = cur.fetchall()		#返回多条用户数据为嵌套元组类型
		#循环该元组,定义一个空的字典'user'{key:字段名,value:单条数据[索引]}，定义一个空的列表'users'[{key:字段名,value:单条数据[索引]},{key:字段名,value:单条数据[索引]}]
		#[{'mobile': u'1344444444', 'email': u'reboot@126.com', 'name_cn': u'kaibinyuan', 'id': 2L, 'name': u'yuanbinbin'}, 
		# {'mobile': u'13888888', 'email': u'haojing@mofanghr.com', 'name_cn': u'taotao', 'id': 3L, 'name': u'pangyantao'}]
        #for row in result:
        #    user = {}
        #    for i, k in enumerate(fields):
        #        user[k] = row[i]
        #    users.append(user)    
	users = [ dict((k,row[i]) for i, k in enumerate(fields)) for row in result]
        return  render_template('userlist.html', users = users)
	#获取数据失败,返回注册页面并抛出异常'errmsg'
    except:
        errmsg = "select userlist failed" 
        print traceback.print_exc()
        return  render_template("userlist.html",result=errmsg)

# 获取单个用户信息，注册成功传name作为where条件，查询这条数据，更新操作需要传id来获取数据，
@app.route('/userinfo')
def userinfo():
	#将前端传来的'id'和'name'保存到字典where中
    where = {}
    where['id'] = request.args.get('id',None)
    where['name'] = request.args.get('name',None)
	#如果没有传入'id'或者'name'则抛出异常'errmsg'并返回'index.html'
    if not where['id']  and not where['name']:
        errmsg  = "must hava a where"
        return render_template('index.html', result = errmsg )
	#如果传进来'id'但是没有传入'name'则condition = 'id = where[id]'(字典的格式化输出)
    if where['id'] and not where['name']:
       condition = 'id = "%(id)s"' % where
	#如果传进来'name'但是没有传入'id'则condition = 'name = where[name]'(字典的格式化输出)
    if where['name'] and not where['id']:
       condition = 'name = "%(name)s"' % where
	#定义需要查询的字段,并执行sql
    fields = ['id', 'name', 'name_cn', 'email', 'mobile']
	#从数据库中获取个人信息
    try:
        sql = "select %s from users where %s" % (','.join(fields),condition)
        cur.execute(sql)
        res = cur.fetchone()#返回一个一阶元组((u'mofang', u'mofang', u'123', u'haojing@mofanghr.com'),)
		#定义一个空的字典'user',循环字段'fields',拼接字段'user' {'fields[key]':'res[index]'}
        user = {}
        for i,k in enumerate(fields):    
            user[k]=res[i]   
        return  render_template('index.html', user = user)
	#获取用户信息失败,抛出异常'errmsg'，返回个人信息页面
    except:
        errmsg  = "get one failed"
        print traceback.print_exc()
        return render_template("index.html",result=errmsg)

# 更新操作，两步 1：get请求显示更新页面并获取要更新数据的信息，2：点击按钮POST请求，执行sql完成更新，成功
# 跳转userlist页面，否则在更新页面输出错误信息。生产环境分两个场景，个人修改自己的信息， 管理员可以更新所
# 有人，暂且不分
@app.route('/update',methods=['GET','POST'])
def update():
	#如果请求的方式为post
    if request.method == "POST":
        print request.form          # 这是个高级写法，把请求内容直接搞成字典，课上会细讲,打印看看长啥样
        data = dict(request.form)   # 转为字典打印出来看张啥样
        print data                  # {'status': [u'0'], 'role': [u'admin'], 'name': [u'xiaohong'], 'mobile': [u'13688888888'] ...}
		#"for k,v in data.items()" = "status [u'0'],mobile [u'13688888888'],role [u'admin'] ..."
		#"(k,v[0])" = "status 0,mobile 13688888888,role admin ..."
		#"%s='%s'" = status = 0
		#condition = ['status=0','mobile=13688888888','role'=admin ...]
        conditions = [ "%s='%s'" %  (k,v[0]) for k,v in data.items()]	
        sql = "update users set %s where id = %s" % (','.join(conditions),data['id'][0])
        print sql
        cur.execute(sql)
        return redirect('/userlist')
	#如果请求的方式不为post
    else:
	   #获取用户个人id,如果前端没有传递进来'id'则抛出异常'errmsg'并且返回更新页面
       id = request.args.get('id',None)
       if not id:
           errmsg = "must hava id"
           return render_template("update.html",result=errmsg)
	   #尝试从数据库中获取个人信息
       fields = ['id', 'name', 'name_cn', 'email', 'mobile'] 
       try:
           sql = "select %s from users where id = %s " % (','.join(fields),id)
           cur.execute(sql)
           res = cur.fetchone()#返回一个一阶元组((u'mofang', u'mofang', u'123', u'haojing@mofanghr.com'),)
		   #定义一个空的字典'user',循环字段'fields',拼接字段'user' {'fields[key]':'res[index]'}
           user = {}
           for i,k in enumerate(fields):    
               user[k]=res[i]
		   #将个人信息user传递到前端页面'update.html'
           return  render_template('update.html', user = user)
	   #从数据库中获取个人信息失败抛出异常'errmsg'并返回'update.html'
       except:
           errmsg = "get one failed"
           print traceback.print_exc()
           return  render_template("update.html",result=errmsg)
 
# 删除，只有传入一个id作为where条件即可，删除成功挑战userlist，生产环境中管理员才有权限，本课暂不区分
@app.route('/delete',methods=['GET'])
def delete():
	#获取前端传递过来的'id'
    id = request.args.get('id',None)
	#如果'id'不存在,则抛出异常'errmsg'并返回用户列表页面
    if not id:
          errmsg = "must hava id" 
          return render_template("userlist.html",result=errmsg)
	#尝试从数据库中删除该用户数据,然后返回用户列表页面
    try:
        sql = "delete from users where id = %s" % id
        cur.execute(sql)
        return redirect('/userlist ')
	#如果尝试不成功则抛出异常'errmsg',然后返回用户列表页面
    except:
        errmsg = "delete failed" 
        return render_template("userlist.html",result=errmsg)

@app.route('/login',methods=['GET','POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('password')
    if not name and not pwd:
	errmsg = "username and password not null"
	return render_template('login.html',result=errmsg)
    if not name and pwd:
	errmsg = "username not null"
	return render_template('login.html',result=errmsg)
    if not name and pwd:
	errmsg = "password not null"
	return render_template('login.html',result=errmsg)
    fields = ['id', 'name', 'password']
    try:
	sql = "select %s from users where name=%s" %(','.join(fields),name)
	cur.execute(sql)
	res = cur.fetchone()
	user = {}
	for i,k in enumerate(fields):
	    user[k]=res[i]
	if name in user:
	    if pwd == user[name]:
		id = user['id']
		return redirect('/userinfo ',id = id)
	    else:
		errmsg = "password not correct"
		return render_template('login.html',result=errmsg)
	else:
	    errmsg = "user not found"
	    return render_template('login.html',result=errmsg)
    except:
	errmsg = "login failed" 
	return render_template("login.html",result=errmsg)

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888,debug=True)
