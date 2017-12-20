#!/usr/bin/env python3

import re

def bracketParser(data):
    if data[0] == '(':
        return (data[0], data[1 : ])

def spaceParser(data):
    matched_space = re.match('\s+', data)
    if matched_space:
        return (' ', data[matched_space.end() : ])

def numberParser(data):
    matched_number = re.match('(?:\d+)(?:\.\d+)?[^)\s]*', data)
    if matched_number:
        try:
            return (int(data[ : matched_number.end()]), data[matched_number.end() : ])
        except:
            try:
                return (float(data[ : matched_number.end()]), data[matched_number.end() : ])
            except:
                return (data[ : matched_number.end()], data[matched_number.end() : ])

def symbolParser(data):
    matched_symbol = re.match('(?:[?a-zA-Z_!]+|[+]|[-]|[*]|[/]|(<=)|(>=)|(>)|(<)|(=))[^)\s]*', data)
    if matched_symbol:
        return (data[ : matched_symbol.end()], data[matched_symbol.end() : ])

def listExpressionParser(data):
    result = valueParser(data)
    token = result[0]
    data = result[1]

    if token == '(':
        parsed_list = []

        try:
            while data[0] != ')':
                res = listExpressionParser(data)
                token = res[0]
                data = res[1]
                if token == ' ':
                    continue
                parsed_list.append(token)

            data = data[1 : ]
            return (parsed_list, data)
        except:
            return "Incorect Syntax: ')' outer parenthesis missing"

    else:
        return (token, data)


def entryExitFunction(data):
    if len(data) == 0:
        return "No Data"

    result = spaceParser(data)
    if result:
        data = result[1]
    result = listExpressionParser(data)
    
    if isinstance(result, tuple) and result[1] != '':
        res = spaceParser(result[1])
        if res and res[1] == '':
            return (result[0], res[1])
        return "not a valid syntax"
    return result

def parser(*args):
    def parserData(data):
        for one_parser in args:
            res = one_parser(data)
            if res:
                return res
    return parserData

valueParser = parser(spaceParser, bracketParser, numberParser, symbolParser)

if __name__ == '__main__':
    '''file_name = input("enter the file name: ")
    with open(file_name, 'r') as file_obj:
        data = file_obj.read()'''
    parsed_data = entryExitFunction('((define circle-area (lambda (r) (* pi (* r r))))(circle-area (+ 5 5)))')
    print(parsed_data[0])
    #'(begin (define r 10) (* pi (* r r)))'