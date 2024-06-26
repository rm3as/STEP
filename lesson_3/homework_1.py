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

def read_multiply(line, index): # "*"をtokenに変換
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_devide(line, index): # "/"をtokenに変換
    token = {'type': 'DEVIDE'}
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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens



def evaluate(tokens):
    def evaluate_mul_dev(tokens): # 最初に掛け算割り算する
        index = 1
        while index < len(tokens):
            if tokens[index]['type'] == 'MULTIPLY':
                part_result = tokens[index - 1]['number'] * tokens[index + 1]['number']
                tokens[index - 1]['number'] = part_result # ex. 5*3 → 15 token上で書き換える
                del tokens[index : index + 2]
            elif tokens[index]['type'] == 'DEVIDE':
                part_result = tokens[index - 1]['number'] / tokens[index + 1]['number']
                tokens[index - 1]['number'] = part_result # ex. 4/2 → 2 token上で書き換える
                del tokens[index : index + 2]
            else:
                index += 1
        return tokens
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
    test("4+2*5") # 掛け算を後ろに書いても、掛け算から計算してくれるか
    test("4/2*1+2") # 割り算ができるか、掛け算と割り算連続でできるか
    test("2") # (一応)極端な例
    test("5.2+3*5.4+1") # 少数の掛け算割り算ができるか
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)