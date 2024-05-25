#! /usr/bin/python3
import math

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

def read_abs(line, index): # absをtokenに直す
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index): # intsをtokenに直す
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index): # roundをtokenに直す
    token = {'type': 'ROUND'}
    return token, index + 5

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
        elif line[index : index + 3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index : index + 3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index : index + 5] == 'round':
            (token, index) = read_round(line, index)
        
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
            if tokens[index]['type'] == 'BRA':
                bracket_count += 1
                bra_index = index
                index += 1
                part_line_index = bra_index
                
                while part_line_index < len(tokens) and bracket_count != 0:
                    part_line_index += 1
                    if tokens[part_line_index]['type'] == 'BRA':
                        bracket_count += 1
                    elif tokens[part_line_index]['type'] == 'CKET':
                        bracket_count -= 1
                cket_index = part_line_index
                part_tokens = tokens[bra_index + 1 : cket_index]
                # print(f"part_tokens:\n{part_tokens}")
                part_result = evaluate(part_tokens)
                tokens[bra_index] = {'type': 'NUMBER', 'number': part_result}
                del tokens[bra_index + 1 : cket_index + 1] # ex. (5+3)→8 token上で書き換える
            else:
                index += 1
        return tokens
    
    def format_number(tokens): # abs, int, roundを計算
        index = 0
        while index < len(tokens):
            part_result = None
            # abs nun, int num, round numをそれぞれ計算
            if tokens[index]['type'] == 'ABS':
                part_result = abs(tokens[index + 1]['number'])
            elif tokens[index]['type'] == 'INT':
                part_result = math.floor(tokens[index + 1]['number'])
            elif tokens[index]['type'] == 'ROUND':
                part_result = round(tokens[index + 1]['number'])
            # token上で書き換える ex. int 5.9 → 5
            if part_result is not None:
                tokens[index] = {'type': 'NUMBER', 'number': part_result}
                del tokens[index + 1]
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
    # print(tokens)
    tokens = evaluate_bracket(tokens)
    tokens = format_number(tokens)
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
    test("(5+3.4)*2/1+(4+2)/2")
    test("int(5.3)")
    test("round(5+3.9)*2+4")
    test("int(5+3.4)/abs(5-9)*2+4")
    
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)