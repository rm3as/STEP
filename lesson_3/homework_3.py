#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_devide(line, index):
    token = {'type': 'DEVIDE'}
    return token, index + 1

def read_bra(line, index):
    token = {'type': 'BRA'}
    return token, index + 1

def read_cket(line, index):
    token = {'type': 'CKET'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_devide(line, index)
        elif line[index] == '(':
            (token, index) = read_bra(line, index)
        elif line[index] == ')':
            (token, index) = read_cket(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens



def evaluate(tokens):
    def evaluate_bracket(tokens):
        index = 0
        bracket_count = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'BRA': # 対応するケットがでてきたら
                bracket_count += 1
                index += 1
                part_line_index_begin = index
                while index < len(tokens) and bracket_count != 0:
                    if tokens[index]['type'] == 'BRA':
                        bracket_count += 1
                    elif tokens[index]['type'] == 'CKET':
                        bracket_count -= 1
                    index += 1
                    print(bracket_count)
                part_line_index_end = index - 1
                part_tokens = tokens[part_line_index_begin : part_line_index_end]
                print(f"part_tokens:\n{part_tokens}")
                part_ans = evaluate(part_tokens)
                tokens[part_line_index_begin - 1] = {'type': 'NUMBER', 'number': part_ans}
                del tokens[part_line_index_begin : part_line_index_end + 1]
                index = part_line_index_begin + 1
                
            else:
                index += 1
        return tokens
        
    def evaluate_mul_dev(tokens):
        index = 1
        while index < len(tokens):
            if tokens[index]['type'] == 'MULTIPLY':
                part_result = tokens[index - 1]['number'] * tokens[index + 1]['number']
                tokens[index - 1]['number'] = part_result
                del tokens[index : index + 2]
            elif tokens[index]['type'] == 'DEVIDE':
                part_result = tokens[index - 1]['number'] / tokens[index + 1]['number']
                tokens[index - 1]['number'] = part_result
                del tokens[index : index + 2]
            else:
                index += 1
        return tokens
    print(tokens)
    tokens = evaluate_bracket(tokens)
    tokens = evaluate_mul_dev(tokens)
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax:')
                print(tokens[index - 1]['type'])
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("4+2*5")
    test("4/2*1+2")
    test("5+3.2*5+1.7")
    test("(5+3)*2")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)