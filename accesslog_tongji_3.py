#!/usr/bin/env python
#coding:utf-8
'''
  功能: 统计同一个IP访问同一个url最多的前10
  获取 IP 和 Url
'''
res = {}
with open('/root/access.log') as f:
    for line in f:
        tmp = line.split(' ')
        ip,url = tmp[0],tmp[6]
        res[(ip,url)] = res.get((ip,url),0)+1
#print res

#ip count done
res_list = res.items()
#print res_list

#maopao
for j in range(10):
    for i in range(len(res_list)-1):
      if res_list[i][1] > res_list[i+1][1]:
        res_list[i],res_list[i+1] = res_list[i+1],res_list[i]

#for r in res.items():
#    print r
#res_list.reverse()
#print res_list[:10]
i = 0
html_str = '<table border="1px">'
html_str += ("<th style='border:solid 1px'>Ranking</th><th style='border:solid 1px'>IP</th></th><th style='border:solid 1px'>Uri</th><th style='border:solid 1px'>Number</th>")
res_list.reverse()
for r in res_list[:10]:
    i = i+1
#    print 'No:%s is %s,count is %s' %(i,r[0],r[1])
    html_str += '<tr><td>No.%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>' %(i,r[0][0],r[0][1],r[1])
html_str +='</table>'

html_f = open('res.html','w')
html_f.write(html_str)
html_f.close()
