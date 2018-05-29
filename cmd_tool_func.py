import os, json
input_func = input
output = None
cons_wrapper = None
running_func = None

class Back_Exit(Exception):
    pass

try:
    f = open("cmd_tool.json", "r")
    user_data = json.load(f)
    f.close()
except:
    user_data = {"user":[], "host":[], "dir":["~", "desktop"], "host_dir":["~", "desktop"], "config":[], "command":["", "python3 cmd_tool.py"]}

def wrapper(f):
    global cons_wrapper
    if cons_wrapper == None:
        def func(*args):
            f(*args)
    else:
        def func(*args):
            cons_wrapper(0)
            f(*args)
            cons_wrapper(1)
    return func

def choose(name_str, name_var):
    res = input_func("{}: ({}) ".format(name_str, str(", ".join("{}:'{}'".format(i, u) for i, u in enumerate(name_var)))))
    if not res:
        res = name_var[0]
    elif res.isdigit() and 0 <= int(res) < len(name_var):
        res = name_var[int(res)]
    return res

def help():
    '''Following commands can be used (*in development):

    help        opens this help page
    scp         opens scp with custom account
    -judge_up   uploads a file to judge-Folder of CoMa-Account
    ssh         initiates connection with custom account
    password    generates key and copys key to server
    *lp         prints a document
    *update     installs or updates cmd_tool on ssh server
    settings    sets preferences / usersettings
    exit        finish program
    
    tipp        CTRL+C stops the execution'''
    if input_func == input:
        print(help.__doc__)
    else:
        input_func("continue")

def ssh():
    '''input the username and host
    manually: ssh <user>@<host> <command>'''
    user = choose("username", user_data["user"])
    host = choose("hostname", user_data["host"])
    command = choose("command", user_data["command"])
    wrapper(os.system)("ssh {}@{} {}".format(user, host, command)) # &

def scp():
    '''input the username and host
    manually: scp <file_dir>/<file> <user>@<host>:<host_dir>/<file>'''
    user = choose("username", user_data["user"])
    host = choose("hostname", user_data["host"])
    file_dir = choose("file direction", user_data["dir"])
    name = input_func("(complete) file-name: ")
    host_dir = choose("host direction", user_data["host_dir"])
    new_name = choose("new file-name", [name])
    wrapper(os.system)("scp {}/{} {}@{}:{}/{}".format(file_dir, name, user, host, host_dir, new_name))

def lp():
    '''print a file'''
    file_name = input_func("file")
    printer = choose("printer", user_data["printer"])
    wrapper(os.system)("lp -d {} {}".format(printer, file_name))

def judge_up():
    '''input the name of file and number, used for CoMa on TU-Berlin, needs a judge folder on Desktop.
    manually: scp <file>.py <user>@<host>:Desktop/judge/<number>.py'''
    name = input_func("name of File: ")
    number = input_func("number of PA: ")
    user = choose("username", user_data["user"])
    host = choose("hostname", user_data["host"])
    wrapper(os.system)("scp {}.py {}@{}:Desktop/judge/{}.py".format(name, user, host, number))

def password():
    '''generates key and copys it to server
    manually: ssh-keygen
    and: ssh-copy-id <user>@<host>'''
    if choose("generate key?", ["yes", "no"]) == "yes":
        wrapper(os.system)("ssh-keygen")
    user = choose("username", user_data["user"])
    host = choose("hostname", user_data["host"])
    wrapper(os.system)("ssh-copy-id {}@{}".format(user, host))

def update():
    '''installs or updates cmd_tool on an ssh server of your choice, so that you can continue running this tool there.'''
    pass

def settings():
    """add new username, host, whatever, and with standard flag - all saved to cmd_tool.json"""
    global output
    print("inside")
    mode = choose("What do you want to change?", ["save", *user_data.keys()])
    while mode in user_data:
        output = "\n".join(("{} - {}".format(i, n) for i,n in enumerate(user_data[mode])))
        if input_func == input:
            print(output)
        act = choose("action", ["new", "swap", "del"])
        if act not in ["new", "swap", "del"]:
            break
        if act == "new":
            name = input_func("text: ")
            user_data[mode].append(name)
        elif act == "swap":
            pair = int(input_func("First: ")), int(input_func("Second: "))
            user_data[mode][pair[0]], user_data[mode][pair[1]] = user_data[mode][pair[1]], user_data[mode][pair[0]]
        else:
            pos = int(input_func("which one: "))
            user_data[mode] = user_data[mode][:pos] + user_data[mode][pos+1:]
        mode = choose("What do you want to change?", ["save", *user_data.keys()])
    with open("cmd_tool.json", "w") as f:
        json.dump(user_data, f)
    output = None

dic = {"help": help, "ssh": ssh, "judge_up": judge_up, "exit": exit, "scp": scp, "settings": settings, "password": password}

def search(inp):
    if inp in dic:
        global running_func
        running_func = dic[inp]
        try:
            running_func()
        except Back_Exit:
            pass
        finally:
            running_func = None
            return True
    else:
        return False
