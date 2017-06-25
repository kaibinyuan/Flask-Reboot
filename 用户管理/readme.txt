1. api.py 读取文件并将用户密码存为字典
2. Flask 调用 api.py 拿到存放所有用户信息的字典,并将自定传递到前端 HTML 
3. Html 将Flask传来的字典通过jinja2渲染
4. pickle.dump(dict,file) 把字典转为二进制存入文件
5. pickle.load(file) 把文件二进制内容转为字典
