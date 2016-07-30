#!/usr/bin/env python
#coding:utf-8

from flask import Flask,request,render_template
#new app
app = Flask(__name__)

@app.route('/')
def index():
    return '<button>hello flask</button>'
@app.route('/reboot')
def reboot():
    word = request.args.get('word','reboot')
    names = [{'name':'xiaoming','age':12},{'name':'wd','age':2}]
    return render_template('test.html',word=word,age=12,names=names)
    #f = open('templates/test.html')
    #content = f.read()
    #f.close()
    #return content

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)
