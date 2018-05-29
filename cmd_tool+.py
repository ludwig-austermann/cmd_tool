#!/usr/bin/python3
try:
    import curses, curses.textpad
    import cmd_tool_func as tool
except ImportError:
    input("platform doesnt support curses. Use cmd_tool.py instead.")
    exit()

def init_curses():
    stdsrc = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdsrc.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    #stdsrc.bkgd(curses.color_pair(1))
    return stdsrc

stdsrc = init_curses()
maxy, maxx = stdsrc.getmaxyx()
mwin = curses.newwin(3, maxx, 0, 0)
main = curses.newwin(maxy-4, maxx, 3, 0)
cons = curses.newwin(1, maxx, maxy-1, 0)

word = ""
message = ""

def show_menu(win):
    head = tool.running_func
    if not head:
        back = "exit"
        head = "<CMD_TOOL+.py>"
    else:
        head = tool.running_func.__name__.upper()
        back = "back"

    win.clear()
    win.bkgd(curses.color_pair(3))
    win.box()
    win.addstr(1, 2, "F1:", curses.A_UNDERLINE)
    win.addstr(1, 6, "help")
    win.addstr(1, 20, "F10:", curses.A_UNDERLINE)
    win.addstr(1, 25, back)
    win.addstr(1, 40, head, curses.A_BOLD)
    win.refresh()

def show_main(win):
    global message
    win.clear()
    win.bkgd(curses.color_pair(4))
    win.box()
    if not tool.running_func:
        win.addstr(1, 2, "Select a command/option:", curses.A_UNDERLINE)
        win.addstr(2, 6, "type help for a list of commands", curses.color_pair(1))
    elif tool.output:
        for i, line in enumerate(tool.output.splitlines()):
            win.addstr(i + 1, 5, line)
    else:
        for i, line in enumerate(tool.running_func.__doc__.splitlines()):
            #meta = line.split(":")
            #win.addstr(i + 1, 5, meta[0], curses.color_pair(1))
            #win.addstr(i + 1, 10, meta[1].split("-")[1])
            win.addstr(i + 1, 5, line)
    
    win.addstr(maxy-5, 1, message)
    win.refresh()

def show_console(win, word):
    win.clear()
    win.bkgd(curses.color_pair(3))
    #text = curses.textpad.Textbox(win)
    #win.addstr(0, 10, text.edit())
    win.addstr(0, 1, ": " + word)
    if word == "":
        win.addstr(0, 3, "", curses.color_pair(1))
    else:
        for k in tool.dic:
            if word in k[:len(word)]:
                win.addstr(0, len(word)+3, k[len(word):], curses.color_pair(1))
                break
    win.refresh()

def input_do(x):
    global message
    message = x
    return main_loop()

def wrap(x):
    global stdsrc #new
    if x:
        init_curses()
    else:
        stdsrc.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

tool.input_func = input_do
tool.cons_wrapper = wrap

def main_loop():
    global message, word
    while True:
        stdsrc.clear()
        stdsrc.refresh()
        show_menu(mwin)
        show_main(main)
        show_console(cons, word)
        c = stdsrc.getch()
        if c == curses.KEY_F1:
            tool.help()
        elif c == curses.KEY_F10:
            if tool.running_func:
                raise tool.Back_Exit()
            break
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            inp, word = word, ""
            if tool.running_func:
                message = ""
                return inp
            if tool.search(inp):
                message = ""
            else:
                message = "invalid input"
        elif chr(c) == "\t":
            for k in tool.dic:
                if word in k[:len(word)]:
                    word = k
        elif c == curses.KEY_BACKSPACE:
            word = word[:-1]
        else:
            word += chr(c)

main_loop()

stdsrc.keypad(0)
curses.echo()
curses.nocbreak()
curses.endwin()