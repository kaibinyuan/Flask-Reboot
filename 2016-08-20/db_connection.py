#!/usr/bin/env python
# coding: utf-8

import MySQLdb as mysql

conn=mysql.connect(user='root',host='127.0.0.1',passwd='123456',db='reboot',charset='utf8')
conn.autocommit(True)
curs = conn.cursor()


#Add
def sql_add(fields,data):
    try:
        #sql = "insert into users (%s) values ('%s')"%(",".join(fields.keys()),"','".join(fields.values()))
    	sql = 'INSERT INTO users (%s) VALUES (%s)' % (','.join(fields), ','.join(['"%s"' % data[x] for x in fields]))
	#print sql
    	curs.execute(sql)
    	conn.commit()
    except:
	print "insert failed"
	return "ERROR"

#Delete
def sql_delete(uid):
    try:
        sql = "delete from users where id=%s"%uid
	print sql
        curs.execute(sql)
        conn.commit()
    except:
	print "delete failed"
        return "ERROR"

#Modify
def sql_modify(modify,condition):
    try:
        #sql = "update users set %s where id = %s" % (','.join(conditions),data['id'][0])
        sql = "update users set %s where %s" % (','.join(modify),condition)
        print sql
        curs.execute(sql)
        conn.commit()
    except:
	print "update failed"
	return "ERROR"

#Select
def sql_select(fields=None,condition=None):
    #print fields,condition
    if condition and fields:
	try:
	    sql = "select %s from users where %s" % (','.join(fields),condition)
	    #print sql
	    curs.execute(sql)
	    result = curs.fetchone()
	    print result
	    return result
	except:
	    print "select failed"
    else:
	try:
            sql = "select %s from users" %','.join(fields)
	    #print sql
	    curs.execute(sql)
	    result = curs.fetchall()
	    print result
	    return result
	except:
	    print "select failed"

if __name__ == '__main__':
#Select One
    fields = ['name', 'password','role']
    condition = 'name="yuanbinbin"'
    sql_select(fields,condition)
#Select All
    #fields = ['id', 'name', 'name_cn', 'email', 'mobile']
    #sql_select(fields)

#Insert
    #fields = ['name','name_cn','mobile','email','role','status','password','create_time']
    #data = {'status': u'0', 'name': u'kafka', 'mobile': u'13688888888', 'name_cn': u'tengine', 'create_time': '2016-08-20 08:22:41', 'role': u'admin', 'password': u'123', 'email': u'nginx@126.com', 'repwd': u'123'}
    #sql_add(fields,data)

#Delete
   #uid = 7
   #sql_delete(uid)

#Modify
    #data = {'status': [u'0'], 'role': [u'admin'], 'name': [u'yuanbinbin'], 'mobile': [u'13681103248'], 'name_cn': [u'nimei'], 'id': [u'2'], 'email': [u'reboot@126.com']}
    #modify = [ "%s='%s'" %  (k,v[0]) for k,v in data.items()]
    #condition = 'id="%s"' % data['id'][0]
    #sql_modify(modify,condition)
