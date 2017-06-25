from flask import Flask,request,render_template,redirect
import user_file
#new app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    name = request.args.get('name')
    pwd = request.args. get('password')
    if name != '' and pwd != '':
        user_file.register('user.txt','a+',name,pwd)
    return redirect('/showuser')

@app.route('/showuser')
def showuser():
    users = user_file.showuser('user.txt')
    return render_template('user.html', users = users)

@app.route('/deluser')
def deluser():
    username = request.args.get('username')
    user_file.deluser('user.txt','r+','w',username)
    return redirect('/showuser')

@app.route('/login')
def login():
    name = request.args.get('name')
    pwd = request.args.get('password')
    res_dict = user_file.res_dict('user.txt',name,pwd)
    if name not in res_dict:
        return "wrong name"
    elif pwd != res_dict[name]:
        return "wrong password"
    else:
        return "login success"
	
@app.route('/modify')
def modify():
    name = request.args.get('username')
    pwd = request.args. get('password')
    return render_template('user_modify.html',username = name,password = pwd)
    
@app.route('/edit')
def edit():
    name = request.args.get('name')
    pwd = request.args.get('password')
    user_file.edit('user.txt','w+',name,pwd)
		
    return redirect('/showuser')
		    
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092,debug=True)
