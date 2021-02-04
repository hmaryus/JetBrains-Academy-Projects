import operator
import re


def commands_action(command):
    if command not in ['/help', '/exit']:
        print('Unknown command')
    elif command == '/exit':
        print("Bye!")
        exit()
    elif command == '/help':
        print('The program calculates the addition and subtraction of numbers')


def format_the_expression(expression):
    expression = expression.split()

    for op in expression:
        if op.startswith('-'):
            if len(op) % 2 == 0:
                expression[expression.index(op)] = '+'
            else:
                expression[expression.index(op)] = '-'
        elif op.startswith('+'):
            expression[expression.index(op)] = '+'

    expression = ' '.join(expression)

    expression = re.sub(r'\((\w)', r'( \1', expression)
    expression = re.sub(r'(\w)\)', r'\1 )', expression)

    return expression


def infix_to_postfix(expression):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = format_the_expression(expression).split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token.isdigit():
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def test_if_correct(command, d={}):
    command = command.replace(' ', '').split('=')
    if 3 > len(command) >= 1:
        if len(command) == 1 and (command[0].isalpha() and command[0] in d.keys()):
            print(d[command[0]])
        elif len(command) == 1 and (command[0].isalpha() and command[0] not in d.keys()):
            print('Unknown variable')
        elif len(command) > 1 and (command[0].isalpha() and command[1].isdigit()):
            d[command[0]] = int(command[1])
        elif len(command) > 1 and (command[0].isalpha() or command[1] in d.keys()):
            try:
                command = [command[0], d[command[1]]]
                d[command[0]] = int(command[1])
            except KeyError:
                print('Invalid identifier')
        else:
            print('Invalid identifier')
    else:
        print('Invalid identifier')


def evaluate_expression(command, d):
    command = command.split()
    new = []

    for i in command:
        if i.isalpha():
            new.append(d[i])
        elif i == '//':
            return 'Invalid expression'
        else:
            new.append(i)

    result = eval(''.join(map(str, new)))
    try:
        return int(result)
    except ValueError:
        return result


def eval_expression(expression, d):
    expression = infix_to_postfix(expression).split()

    result = 0
    stack = []

    for el in expression:
        if el.isalpha():
            stack.append(d[el])
        else:
            try:
                stack.append(int(el))
            except ValueError:
                val1 = stack.pop()
                val2 = stack.pop()
                switcher = {'+': val2 + val1,
                            '-': val2 - val1,
                            '*': val2 * val1,
                            '/': val2 / val1,
                            '^': val2 ** val1}
                stack.append(switcher.get(el))

    return int(stack.pop())



my_dict_values = {}


while True:
    my_input = input()
    try:
        if not my_input:
            continue
        if my_input.startswith('/'):
            commands_action(my_input)
            continue
        if my_input.__contains__('=') or my_input.isalpha():
            test_if_correct(my_input, my_dict_values)
            continue
        try:
            print(evaluate_expression(my_input, my_dict_values))
            continue
        except KeyError:
            print('Unknown variable')
    except NameError:
        print('Unknown variable')
    except SyntaxError:
        print('Invalid expression')
