import string

def parse(data):
    return assembler(tokenizer(data))

def tokenizer(data):
    return data.replace('(', ' ( ').replace( ')', ' ) ').split()


def main():
    data = ''
    file_name = input("enter the file name")
    with open(file_name, 'r') as file_obj:
        for line in file_obj:
            data += line.strip()

    parsed_data = parse(data)
    #result = evaluator(parsed_data)

if __name == '__main__':
    main()


