import os, json
input_func = input
output = None
cons_wrapper = None
running_func = None
temp_values = [] #TODO:

DEFAULT = {"user":[""], "host":[""], "dir":["~", "desktop"], "host_dir":["~", "desktop"], "config":[], "command":["", "python3 cmd_tool.py"], "printer":[""]}

class Back_Exit(Exception):
    pass

class SpecialFunktion:
    def __init__(self, commands, exe, info, tipp):
        self.commands = {k : commands[k][0](*commands[k][1:], parent=self) for k in commands}
        self.execute = exe
        self.info = info
        self.tipp = tipp
    
    @property
    def values(self):
        return [self.commands[c].prefix + self.commands[c].value for c in self.commands if self.commands[c].value != self.commands[c].default]

    def __call__(self):
        self.execute(*self.values)

class OutsideFunktion(SpecialFunktion):
    def __call__(self):
        print("log:", self.code)
        wrapper(os.system)(self.code)
    
    @property
    def code(self):
        return "{} {}".format(self.execute, "".join(self.values))

class Choose:
    def __init__(self, info, data=None, prefix="", default="", parent=None):
        self.info = info
        self.data = data
        self.prefix = prefix
        self.default = default
        self.parent = parent

    def __call__(self):
        if not self.data:
            self.value = input_func(self.info + ": ")
        elif type(self.data) == list:
            self.value = choose(self.info, self.data)
        else:
            self.value = choose(self.info, [self.parent.commands[self.data].value])

class FileFinder:
    def __init__(self, info, parent=None):
        self.info = info
        self.data = os.system()
        self.parent = parent

    def __call__(self):
        self.value = input_func(self.info + ": ")
def line(s_f): #testuses
    for var in s_f.commands:
        s_f.commands[var]()
    s_f()

try:
    f = open("cmd_tool.json", "r")
    user_data = json.load(f)
    f.close()
except:
    user_data = {}
finally:
    for key in DEFAULT:
        if key not in user_data:
            user_data[key] = DEFAULT[key]

def wrapper(f, wait=False):
    global cons_wrapper
    if cons_wrapper == None:
        def func(*args):
            f(*args)
    else:
        def func(*args):
            cons_wrapper(0)
            f(*args)
            if wait:
                input()
            cons_wrapper(1)
    return func

def choose(name_str, name_var):
    res = input_func("{}: ({}) ".format(name_str, str(", ".join("{}:'{}'".format(i, u) for i, u in enumerate(name_var)))))
    if not res:
        res = name_var[0]
    elif res.isdigit() and 0 <= int(res) < len(name_var):
        res = name_var[int(res)]
    return res

def option(text, identifier, default=""): #red
    if text != default:
        return "-{}{} ".format(identifier, text)
    return ""

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

def ssh(): #red
    '''input the username and host
    manually: ssh <user>@<host> <command>'''
    user = choose("username", user_data["user"])
    host = choose("hostname", user_data["host"])
    command = choose("command", user_data["command"])
    wrapper(os.system)("ssh {}@{} {}".format(user, host, command)) # &

def scp(): #red
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
    '''print a file
    to find out "job-id" run lpstats
    manually: fast print: -d <device> -o <> <file>'''#TODO: manually
    action = choose("What do you want to do?", ["fast print", "advanced print", "show printers", "lpstats", "cancel printing", "release"])
    if action == "show printers":
        wrapper(os.system, True)("lpstats -p -d")
    elif action == "lpstats":
        wrapper(os.system, True)("lpstats")
    elif action == "cancel printing":
        job_id = input_func("job-id: ")
        wrapper(os.system)("cancel {}".format(job_id))
    elif action == "release":
        job_id = input_func("job-id: ")
        wrapper(os.system)("lp -i {} -H resume".format(job_id))
    elif action == "fast print":
        file_name = input_func("filename: ")
        printer = option(choose("printer", user_data["printer"]), "d ")
        bothsided = option(choose("one sided?", ["one-sided", "two-sided-short-edge", "two-sided-long-edge"]), "o sides=", "one-sided")
        fit = option(choose("scale", ["", "fit-to-page"]), "o ")
        wrapper(os.system)("lp {}{}{}{}".format(printer, bothsided, fit, file_name))
    elif action == "advanced print":
        file_name = input_func("filename: ")
        printer = option(choose("printer", user_data["printer"]), "d ")
        num = option(choose("number of copies", ["0"]), "n ", "0")
        media = option(choose("papersize", ["A4", "Letter"]), "o media=")
        landscape = option(choose("orientation", ["", "landscape"]), "o ")
        bothsided = option(choose("one sided?", ["one-sided", "two-sided-short-edge", "two-sided-long-edge"]), "o sides=", "one-sided")
        holding = option(choose("when", ["now", "12:00", "weekend", "night", "day", "indefinite"]), "o job-hold-until=", "now")
        priority = option(choose("priority", ["", "1", "100"]), "o job-priority=")
        order = option(choose("output order", ["normal", "reversed"]), "o outputorder=", "normal")
        page_range = option(choose("page range", ["", "1,3,5", "1-5"]), "o page-range=")
        num_up = option(choose("how many pages per page", ["1", "2", "4", "6", "9", "16"]), "o number-up=", "1")
        border = option(choose("border", ["none", "single", "single-thick", "double", "double-thick"]), "o page-border=", "none")
        fit = option(choose("scale to fit?", ["", "fit-to-page"]), "o ")
        #TODO: count
        wrapper(os.system)("lp {}{}{}{}{}{}{}{}{}{}{}{}{}".format(printer, num, media, landscape, bothsided, holding, priority, order, page_range, num_up, border, fit, file_name))

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

dic = {"help": help, "ssh": ssh, "judge_up": judge_up, "exit": exit, "scp": scp, "settings": settings, "password": password, "lp": lp}

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
    if inp and ":" == inp[0]:
        if running_func:
            if inp[1:] == "info":
                output(running_func.info)
            elif inp[1:] == "tipp":
                output(running_func.)
            return True
    return False

FUNCTIONS = {
    "help": SpecialFunktion({}, lambda : print(FUNCTIONS["help"].info) if input_func == input else input_func("continue"), '''Following commands can be used (*in development):\n
    help        opens this help page
    scp         opens scp with custom account
    -judge_up   uploads a file to judge-Folder of CoMa-Account
    ssh         initiates connection with custom account
    password    generates key and copys key to server
    *lp         prints a document
    *update     installs or updates cmd_tool on ssh server
    settings    sets preferences / usersettings
    exit        finish program''', "CTRL+C stops the execution")
    "ssh": OutsideFunktion({
        "user"   : (Choose, "username", user_data["user"]),
        "host"   : (Choose, "hostname", user_data["host"], "@")},
        "ssh", "initiates ssh connection", "manually: ssh <user>@<host> <command>"),
    "scp": OutsideFunktion({
        "dir"    : (Choose, "file directory", user_data["dir"]),
        "file"   : (Choose, "(complete) filename", None, "/"),
        "user"   : (Choose, "username", user_data["user"], " "),
        "host"   : (Choose, "hostname", user_data["host"], "@"),
        "hdir"   : (Choose, "host directory", user_data["host_dir"], ":"),
        "newname": (Choose, "new filename", "file", "/")},
        "scp", "copies files over ssh", "manually: scp <file_dir>/<file> <user>@<host>:<host_dir>/<file>"),
    "lp": SpecialFunktion({
        "f"      : (Choose, "function", ["fast", "advanced", "printers", "stats", "cancel", "release"], "lp ")},
        search, 'shortcut to print commands, to find out "job-id" run lpstats', ""),
    "lp fast": OutsideFunktion({
        "file"   : (Choose, "filename"),
        "printer": (Choose, "printer", user_data["printer"], "d "),
        "b-sided": (Choose, "one sided?", ["one-sided", "two-sided-short-edge", "two-sided-long-edge"], "o sides", "one-sided"),
        "fit"    : (Choose, "scale", ["", "fit-to-page"], "o ")},
        "lp", "prints a file with predefined options", "manually: fast print: -d <device> -o <> <file>")
    "lp advanced": OutsideFunktion({
        "file"   : (Choose, "filename"),
        "printer": (Choose, "printer", user_data["printer"], "d "),
        "num"    : (Choose, "number of copies", None, "n "),
        "landsc" : (Choose, "orientation", ["", "landscape"], "o "),
        "b-sided": (Choose, "one sided?", ["one-sided", "two-sided-short-edge", "two-sided-long-edge"], "o sides=", "one-sided"),
        "holding": (Choose, "when", ["now", "12:00", "weekend", "night", "day", "indefinite"], "o job-hold-until=", "now"),
        "prio"   : (Choose, "priority: (1-100)", None, "o job-priority=")
        "fit"    : (Choose, "scale", ["", "fit-to-page"], "o ")},
        "lp", "prints a file with predefined options", "manually: fast print: -d <device> -o <> <file>")}