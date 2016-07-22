#!/usr/bin/env python
#coding:utf-8

#Open Log File
nginx_access = open('/root/access.log','a+')
#Read Log File
log = nginx_access.readlines()
#Close Log File
nginx_access.close()

# 将文本拼接成 IP:num 的字典形式
lines = len(log)
host = {}
for number in range(lines):
	IP = log[number].split(' ')[0]
	if IP not in host:
	    host[IP] = 1
	else:
	    host[IP] += 1
#print host

# 字典翻转拼接成 num:IP 的字典形式
result = {}
for k,v in host.items():
	result.setdefault(v,[])
	result[v].append(k)
#print result
print result.keys()

#统计前10名
count = 0
f = open('tongji.html','a+')
f.write("<html><table style='border:solid 1px'>")
f.write("<th style='border:solid 1px'>Number</th><th style='border:solid 1px'>IP</th>")
while count < 10:
	key = max(result.keys())
	print "出现了%s次的IP：%s" % (key,result[key])
	for word in result[key]:
	    f.write('<tr><td style="border:solid 1px">%s</td><td style="border:solid 1px">%s</td></tr>' % (key,word))
	result.pop(key)
	count = count + 1
f.write("</table></html>")
f.close()
