
def showuser(filename):
    with open(filename) as f:
        users = [ line.split(":") for line in f.read().split('\n') ]
        return users

def register(filename,mode,name,pwd):
    with open(filename,mode) as f:
        f.write('%s:%s\n'%(name,pwd))

def deluser(filename,mode1,mode2,username):
    with open(filename,mode1) as f:
        users = f.read().split('\n')
        for user in users:
            if user.split(':')[0] == username:
                users.remove(user)
                with open(filename,mode2) as f:
                    f.write("\n".join(users))

def res_dict(filename,name,pwd):
    d = {}
    with open(filename) as f:
        content = f.readlines()
        for user in content:
             dict_name = user.rstrip("\n").split(":")[0]
             d[dict_name] = user.rstrip("\n").split(":")[1]
	return d

def edit(filename,mode,name,pwd):
    with open(filename) as f:
        users = f.read().split('\n')[:-1]
        for key,user in enumerate(users):
            if user.split(':')[0] == name and user.split(':')[1] != pwd:
                users[key] = name+':'+pwd
                users.append('')
                with open(filename,mode) as f:
                    f.write('\n'.join(users))

            else:
                return "can not modify the name"

