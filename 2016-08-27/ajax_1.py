#coding:utf-8
from flask import Flask,request,render_template

app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():    
    user = {'id':1,'name':'wd','age':18}
    return render_template('ajax.html',user = user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090,debug=True)
