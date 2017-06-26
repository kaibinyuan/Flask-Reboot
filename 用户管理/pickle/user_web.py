from flask import Flask,request,render_template,redirect
import user

app = Flask(__name__)

filename = 'user.txt'
user = user.User(filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    username = request.args.get('name')
    password = request.args. get('password')
    if username != '' and password != '':
        user.modify(username, password)
    return redirect('/showuser')


@app.route('/showuser')
def showuser():
    users = user.all()
    return render_template('user.html', users=users)


@app.route('/deluser')
def deluser():
    username = request.args.get('username')
    user.delete(username)
    return redirect('/showuser')


@app.route('/login')
def login():
    username = request.args.get('name')
    password = request.args.get('password')
    user_info = user.info(username)

    if username not in user_info:
        return "wrong name"
    elif password != user_info[username]:
        return "wrong password"
    else:
        return "login success"


@app.route('/modify')
def modify():
    name = request.args.get('username')
    pwd = request.args. get('password')
    return render_template('user_modify.html', username=name, password=pwd)


@app.route('/edit')
def edit():
    username = request.args.get('name')
    password = request.args.get('password')
    user.modify(username, password)

    return redirect('/showuser')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092, debug=True)
