#!/usr/bin/env python3

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
        'append':  op.add,
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'expt':    pow,
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: List(x), 
        'list?':   lambda x: isinstance(x, List), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, int) or isinstance(x, float),  
        'print':   print,
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
        (_, exp) = x
        return exp

    elif x[0] == 'set!':
        (_, symbol, exp) = x
        if env.has_key(symbol):
            env[symbol] = eval(exp, env)

    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        if eval(test, env):
            return eval(conseq, env)
        else:
            return eval(alt, env)

    elif x[0] == 'define':
        (_, symbol, value) = x
        env[symbol] = eval(value, env)

    elif x[0] == 'lambda':
        (_, params, body) = x
        return procedure(params, body, env)

    else:
        proc = env[x[0]]
        args = [eval(exp, env) for exp in x[1 : ]]
        return proc(*args)

def procedure(parameters, body, env):

    def callFunction(*args):
        arg_list = [i for i in args]
        return eval(body, localEnv(parameters, arg_list, env))
    return callFunction

collective_env = {}

def localEnv(parameters, arg_list, env):
    if len(parameters) != len(arg_list):
        print("number of arguments not equal to the number of parameters")
        #exit()

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