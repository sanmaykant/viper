from sys import argv
from os import getcwd
from os.path import join

from interpreter import Interpreter
from errors import Error
from lexer import Lexer
from parser import Parser

def getCode() -> str:
    line: str = ' '
    lines: str = ''
    while line:
        line = input('viper > ')
        if line == '': break
        if line == 'exit': return 'exit'
        lines += line + '\n'

    return lines

def getPath():
    try: return join(getcwd(), argv[1])
    except: return

def execute(srcCode: str):
    srcCode = srcCode.replace('\t', '    ')

    lexer = Lexer(srcCode)
    tokens = lexer.yieldTokens()
    if isinstance(tokens, Error): print(tokens); return

    parser = Parser(tokens, srcCode)
    nodes = parser.parse()
    if isinstance(nodes, Error): print(nodes); return

    interpreter = Interpreter(nodes, srcCode)
    interpreter.traverse()

if __name__ == '__main__':
    path = getPath()
    if path != None:
        with open(path, 'r') as srcFile:
            srcCode = srcFile.read()
        execute(srcCode)
    else:
        while True:
            srcCode = getCode()
            if srcCode == 'exit': break

            execute(srcCode)