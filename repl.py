#!/usr/bin/env python3

from lispInterpreter import eval, standardEnv
from lispParser import entryExitFunction

global_env = standardEnv()

def repl():
    while True:
        prompt = input('lisp>')
        parsed_data = entryExitFunction(prompt)
        if isinstance(parsed_data, tuple):
            val = eval(parsed_data[0], global_env)
        else:
            val = parsed_data
        if val is not None: 
            print(val)

if __name__ == '__main__':
    repl()

