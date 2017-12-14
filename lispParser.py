import re

def bracketParser(data):
    if data[0] == '(':
        return (data[0], data[1 : ].strip())

def spaceParser(data):
    matched_space = re.match('\s+', data)
    if matched_space:
        return (' ', data[matched_space.end() : ].strip())

def numberParser(data):
    matched_number = re.match('(?:\d+)(?:\.\d+)?', data)
    if matched_number:
        try:
            return (int(data[ : matched_number.end()]), data[matched_number.end() : ].strip())
        except:
            try:
                return (float(data[ : matched_number.end()]), data[matched_number.end() : ].strip())
            except:
                return (data[ : matched_number.end()], data[matched_number.end() : ].strip())

def wordParser(data):
    matched_word = re.match('[?a-zA-Z_!]+', data)
    if matched_word:
        return (data[ : matched_word.end()], data[matched_word.end() : ].strip())

def operatorParser(data):
    matched_operator = re.match('(?:[+]|[-]|[*]|[/]|(<=)|(>=)|(>)|(<)|(=))', data)
    if matched_operator:
        return (data[ : matched_operator.end()], data[matched_operator.end() : ].strip())

def listExpressionParser(data):
    result = parser(spaceParser, bracketParser, numberParser, wordParser, operatorParser, input_data = data)
    token = result[0]
    data = result[1].strip()

    if token == ' ':
        return listExpressionParser(data)

    if token == '(':
        parsed_list = []

        while data[0] != ')':
            res = listExpressionParser(data)
            token = res[0]
            if token == ' ':
                continue
            parsed_list.append(token)
            #print("list", parsed_list)
            data = res[1].strip()

        data = data[1 : ].strip()
        return (parsed_list, data.strip())

    else:
        return (token, data.strip())

def parser(*args, input_data):
    for one_parser in args:
        res = one_parser(input_data)
        if res:
            return res
    return None

def main():
    #data = ''
    #file_name = input("enter the file name")
    #with open(file_name, 'r') as file_obj:
    #    for line in file_obj:
    #        data += line.strip()

    parsed_data = listExpressionParser('   ((define x 10)(define y 5)(lambda (x y) (* x y) 5 2)(* x x))')
    print(parsed_data)
    #result = evaluator(parsed_data)

if __name__ == '__main__':
    main()