import math 
import operator as op
from functools import reduce
#from lispParser import listExpressionParser

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

def eval(x, env ):
    if isinstance(x, str):
        return env[x]

    elif isinstance(x, int) or isinstance(x, float):
        return x

    elif x[0] == 'if':
        (_, test, conseq, alt) = x

        if eval(test, env):
            return eval(conseq, env)
        else:
            return eval(alt, env)

    elif x[0] == 'define':
        (_, symbol, value) = x
        env[symbol] = eval(value, env)

    else:
        proc = env[x[0]]
        args = [eval(exp, env) for exp in x[1 : ]]
        return proc(*args)


if __name__ == '__main__':
    print(eval(['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]], global_env))