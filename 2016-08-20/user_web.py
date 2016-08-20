#coding:utf-8

from flask import Flask,request,render_template,redirect,session
import MySQLdb as mysql
import json 
import time
import traceback
from db_connection import *

#固定语法
app = Flask(__name__)
app.secret_key="abcdefg"

#'/register' 路由允许get,post两种方式
@app.route('/register',methods=['GET','POST'])
def register():
#如果请求方式为'post'
    if request.method == 'POST':
        print request.form
 	print dict(request.form)
	data = dict((k,v[0]) for k,v in dict(request.form).items()) #{'status': u'0', 'name': u'nginx', 'mobile': u'1355555555', 'name_cn': u'tengine' ...}
        data["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print data
#数据库操作
        fields = ['name','name_cn','mobile','email','role','status','password','create_time']
        if not data["name"] or not data["password"] or not data["role"]:
            errmsg = 'name or password or role not null'
            return render_template("register.html",result=errmsg)

        if data["password"] != data["repwd"]:
            # return  json.dumps('code':1,'errmsg':'The two passwords you typed do not match.'
            errmsg = 'The two passwords you typed do not match'
            return render_template("register.html",result=errmsg)

	sql_add(fields,data)
	return redirect('/userinfo?name=%s' % data['name'])

@app.route('/userlist')
def userlist():
#    if not session.get('name',None):
#        return redirect('/login')
    users = []
    fields = ['id', 'name', 'name_cn', 'email', 'mobile']
    try:
        result = sql_select(fields)
        users = [ dict((k,row[i]) for i, k in enumerate(fields)) for row in result]
        return  render_template('userlist.html', users = users)
    except:
        errmsg = "select userlist failed" 
        print traceback.print_exc()
        return  render_template("userlist.html",result=errmsg)

@app.route('/userinfo')
def userinfo():
    #if not session.get('name',None):
    #    return redirect('/login')	 
    where = {}
    where['id'] = request.args.get('id',None)
    where['name'] = request.args.get('name',None)
    if not where['id']  and not where['name']:
        errmsg  = "must hava a where"
        return render_template('index.html', result = errmsg )
    if where['id'] and not where['name']:
       condition = 'id = "%(id)s"' % where
    if where['name'] and not where['id']:
       condition = 'name = "%(name)s"' % where

    #从数据库中获取个人信息
    fields = ['id', 'name', 'name_cn', 'email', 'mobile']
    try:
        result = sql_select(fields,condition)
        user = {}
        for i,k in enumerate(fields):    
            user[k]=result[i]   
        return  render_template('index.html', user = user)
    except:
        errmsg  = "get one failed"
        print traceback.print_exc()
        return render_template("index.html",result=errmsg)
	

@app.route('/update',methods=['GET','POST'])
def update():
	#如果请求的方式为post
    if request.method == "POST":
        data = dict(request.form)
        modify = [ "%s='%s'" %  (k,v[0]) for k,v in data.items()]	
	condition = 'id="%s"' % data['id'][0]
	sql_modify(modify,condition)
        #sql = "update users set %s where id = %s" % (','.join(conditions),data['id'][0])
        #print sql
        #cur.execute(sql)
        return redirect('/userlist')
    else:
       id = request.args.get('id',None)
       if not id:
           errmsg = "must hava id"
           return render_template("update.html",result=errmsg)
       fields = ['id', 'name', 'name_cn', 'email', 'mobile'] 
       try:
           #sql = "select %s from users where id = %s " % (','.join(fields),id)
           #cur.execute(sql)
           #res = cur.fetchone()
	   condition = 'id="%s"' % id
   	   result = sql_select(fields,condition)
           user = {}
           for i,k in enumerate(fields):    
               user[k]=result[i]
           return  render_template('update.html', user = user)
       except:
           errmsg = "get one failed"
           print traceback.print_exc()
           return  render_template("update.html",result=errmsg)
 
@app.route('/delete',methods=['GET'])
def delete():
    if not session.get('name',None):
        return redirect('/login')
    id = request.args.get('id',None)
    if not id:
          errmsg = "must hava id" 
          return render_template("userlist.html",result=errmsg)
    try:
	sql_delete(id)
        #sql = "delete from users where id = %s" % id
        #cur.execute(sql)
        return redirect('/userlist')
    except:
        errmsg = "delete failed" 
        return render_template("userlist.html",result=errmsg)

@app.route('/login',methods=['GET','POST'])
def login():
    #如果请求的方式为"POST"方式执行以下
    if request.method == "POST":
	#收集前端收集的post请求参数
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	#如果前端未收集到'name'或者'password'则抛出异常'errmsg'并重定向到'login.html'
	if not data.get('name',None) or not data.get('password',None):
	    errmsg = 'name or password not null'
	    return render_template('login.html',result=errmsg)
	#拼接sql语句,查询数据库
	fields = ['name', 'password','role']
	condition = 'name="%s"' %data['name']
	res = sql_select(fields,condition)
	#sql = 'select %s from users where name ="%s"' % (','.join(fields),data['name'])
	#cur.execute(sql)
	#res = cur.fetchone()
	if not res:
	    errmsg = "%s is not exist" % data['name']
	    return  render_template('login.html',result=errmsg)
	user = {}
	user = dict((k,res[i]) for i,k in enumerate(fields)) #{'password': u'aaa', 'name': u'reboot'}
	if user['password'] != data['password']: 
	    errmsg = 'password is wrong'
	    return render_template('login.html',result=errmsg)
	else:
	    #创建session
	    session['name'] = user['name']
	    session['role'] = user['role']
	    return redirect('/userlist')
    #如果请求的方式为"GET"方式执行以下
    else:
            return render_template('login.html')
#删除session
@app.route('/loginout')
def loginout():
    session.pop('name')
    session.pop('role')
    return redirect('/login')
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888,debug=True)
