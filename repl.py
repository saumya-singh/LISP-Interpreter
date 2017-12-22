#!/usr/bin/env python3
import cmd
import os
from lispInterpreter import eval, standardEnv
from lispParser import entryExitFunction

commands = []
global_env = standardEnv()
class CmdParse(cmd.Cmd):
    prompt = "lisp> "
    def do_listall(self, line):
        print(commands)
    def default(self, line):
        commands.append(line)
        if line == 'exit()':
            os._exit(1)
        parsed_data = entryExitFunction(line)
        if isinstance(parsed_data, tuple):
            val = eval(parsed_data[0], global_env)
        else:
            val = parsed_data
        if val is not None: 
            print(val)

CmdParse().cmdloop()


