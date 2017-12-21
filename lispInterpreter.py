#!/usr/bin/env python3

import os
import math 
import operator as op
from sys import argv
from functools import reduce
from lispParser import entryExitFunction

def standardEnv():
    env = {}
    env.update({
        '+':       lambda *x : reduce((lambda x,y : op.add(x,y)), [i for i in x]),
        '-':       op.sub,
        '*':       lambda *x : reduce((lambda x,y : op.mul(x,y)), [i for i in x]),
        '/':       op.truediv, 
        '>':       op.gt,
        '<':       op.lt, 
        '>=':      op.ge, 
        '<=':      op.le, 
        '=':       op.eq,
        'abs':     abs,
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:],  
        'expt':    pow,
        'length':  len, 
        'map':     map,
        'max':     max,
        'min':     min,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, int) or isinstance(x, float),  
        'procedure?': callable,
        'round':   round,
        'remainder':  op.mod,
        'symbol?': lambda x: isinstance(x, str),
        'pi': 3.141592653589793
        })

    return env

global_env = standardEnv()

def eval(x, env):
    if isinstance(x, str):
        return env[x]

    elif not isinstance(x, list):
        return x

    elif x[0] == 'quote':
        try:
            (_, exp) = x
            return exp
        except:
            print("not a valid syntax: 'quote' does not have valid number of arguments")
            os._exit(1)

    elif x[0] == 'set!':
        try:
            (_, symbol, exp) = x
            if symbol in env.keys():
                env[symbol] = eval(exp, env)
        except:
            print("not a valid syntax: 'set!' does not have valid number of arguments")
            os._exit(1)

    elif x[0] == 'if':
        try:
            (_, test, conseq, alt) = x
            if eval(test, env):
                return eval(conseq, env)
            else:
                return eval(alt, env)
        except:
            print("not a valid syntax: 'if' does not have valid number of arguments")
            os._exit(1)

    elif x[0] == 'define':
        try:
            (_, symbol, value) = x
            env[symbol] = eval(value, env)
        except:
            print("not a valid syntax: 'define' does not have valid number of arguments")
            os._exit(1)

    elif x[0] == 'lambda':
        try:
            (_, params, body) = x
            return procedure(params, body, env)
        except:
            print("not a valid syntax: 'lambda' does not have valid number of arguments")
            os._exit(1)

    else:
        try:
            proc = env[x[0]]
            args = [eval(exp, env) for exp in x[1 : ]]
            return proc(*args)
        except:
            print("not a valid syntax")
            os._exit(1)

def procedure(parameters, body, env):
    def callFunction(*args):
        arg_list = [i for i in args]
        return eval(body, localEnv(parameters, arg_list, env))
    return callFunction

collective_env = {}

def localEnv(parameters, arg_list, env):
    if len(parameters) != len(arg_list):
        print("number of arguments not equal to the number of parameters")
        os._exit(1)
    local_env = {}
    local_var = zip(parameters, arg_list)
    for var_value_pair in local_var:
        local_env[var_value_pair[0]] = var_value_pair[1]
    collective_env.update(local_env)
    collective_env.update(env)
    return collective_env
    
def main():
    #ans = eval(['begin', ['define', 'circle-area', ['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]], ['circle-area', ['+', 5, 95]]], global_env)
    #print(ans)
    file_name = argv[1]
    with open(file_name, 'r') as file_obj:
        data = file_obj.read()
        
    parsed_data = entryExitFunction(data)
    if isinstance(parsed_data, tuple):
        print(eval(parsed_data[0], global_env))
    else:
        print(parsed_data)

if __name__ == '__main__':
    main()