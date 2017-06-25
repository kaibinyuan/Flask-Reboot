#!/usr/bin/env python
#coding:utf-8
'''
  功能: 统计同一个IP访问同一个url最多的前10
  获取 IP 和 Url
'''
#获取IP和URL
def oper_file(file_name):
  res = {}
  with open(file_name) as f:
    for line in f:
        tmp = line.split(' ')
        ip,url = tmp[0],tmp[6]
        res[(ip,url)] = res.get((ip,url),0)+1
  return res.items()
#同一IP访问的同一个URL的数量前十
def bubble_sort(arr,times):
  for j in range(times):
    for i in range(len(arr)-1):
      if arr[i][1] > arr[i+1][1]:
        arr[i],arr[i+1] = arr[i+1],arr[i]
  return arr
#将排序后的元组列表写入Html
def write_html(arr):
  i = 0
  html_str = '<table border="1px">'
  html_str += ("<th style='border:solid 1px'>Ranking</th><th style='border:solid 1px'>IP</th></th><th style='border:solid 1px'>Uri</th><th style='border:solid 1px'>Number</th>")
  arr.reverse()
  for r in arr[:10]:
    i = i+1
    html_str += '<tr><td>No.%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>' %(i,r[0][0],r[0][1],r[1])
  html_str +='</table>'

  html_f = open('res.html','w')
  html_f.write(html_str)
  html_f.close()

def start_operate():
  res_list = oper_file('/root/access.log')
  sort_list = bubble_sort(res_list,11)
  write_html(sort_list)
start_operate()
