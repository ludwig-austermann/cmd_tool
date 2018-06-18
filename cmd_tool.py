import cmd_tool_func as tool

def main():
    print("Welcome to cmd_tool.py.\nType help for a list of commands. <ENTER> to exit.")
    inp = input(">> ")

    while inp:
        if not tool.search(inp):
            print("Invalid input, type help for help.")
        
        inp = input(">> ")

if __name__ == "__main__":
    main()