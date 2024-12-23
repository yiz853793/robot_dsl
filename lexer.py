# lexer.py
# 这个模块是一个词法分析器，用于将输入的代码字符串分解成一系列的标记（tokens）。

import ply.lex as lex
import sys

class Lexer:
    # 定义保留字和它们的标记名称
    reserved = {
        'if':       'IF',
        'begin':    'BEGIN',
        'else':     'ELSE',
        'end':      'END',
        'while':    'WHILE',
        'function': 'FUNCTION',
        'return':   'RETURN',
        'itoa':     'ITOA',
        'atoi':     'ATOI',
        'and':      'AND',
        'or':       'OR',
        'not':      'NOT',
        'true':     'TRUE',
        'false':    'FALSE',
    }
    
    # 定义所有可能的标记
    tokens = [
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGNMENT',
        'EQUAL',
        'NEQ',
        'LEQ',
        'LSS',
        'GEQ',
        'GTR',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'COMMA',
        'NUMBER',
        'ID',
        'STR',
        'CALLPY',
    ] + list(reserved.values())

    # 定义单字符操作符的正则表达式和对应的标记
    t_PLUS          = r'\+'
    t_MINUS         = r'-'
    t_TIMES         = r'\*'
    t_DIVIDE        = r'/'
    t_ASSIGNMENT    = r'='
    t_EQUAL         = r'=='
    t_NEQ           = r'\!='
    t_LEQ           = r'<='
    t_LSS           = r'<'
    t_GEQ           = r'>='
    t_GTR           = r'>'
    t_LPAREN        = r'\('
    t_RPAREN        = r'\)'
    t_LBRACKET      = r'\['
    t_RBRACKET      = r'\]'
    t_COMMA         = r','

    # 定义注释和空格的忽略规则
    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    # 定义数字的解析规则
    def t_NUMBER(self, t):
        r'\d+(\.\d*)?'
        t.value = {'value' : int(t.value), 'type' : 'NUMBER'}
        return t
    
    # 定义标识符的解析规则
    def t_ID(self, t):
        r'[a-zA-Z_][0-9a-zA-Z_]*'
        t.type = self.reserved.get(t.value, 'ID')
        if t.type == 'ID' :
            t.value = {'type' : 'ID', 'value' : t.value}
        elif t.type == 'TRUE':
            t.value = {'type' : 'TRUE', 'value' : True}
        elif t.type == 'FALSE':
            t.value = {'type' : 'FALSE', 'value' : False}
        return t

    # 定义字符串的解析规则
    def t_STR(self, t):
        r'''("((\\\")|[^\n\"])*")|('((\\\')|[^\n\'])*')'''
        t.value = {'value' : t.value[1:-1], 'type' : 'STR'}
        return t

    # 定义调用Python代码的解析规则
    def t_CALLPY(self, t):
        r'./([a-zA-Z]:\\)?([0-9a-zA-Z_]+\\)*[0-9a-zA-Z_]+.py'
        t.value = {'value' : t.value[2:], 'type' : 'CALLPY'}
        return t
    
    # 定义行号跟踪规则
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # 定义错误处理规则
    def t_error(self, t):
        print(f"Illegal character {t.value[0]} in line {t.lexer.lineno}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)  # 构建词法分析器

    def tokenize(self, data):
        """对输入数据进行词法分析，返回标记列表。"""
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # 没有更多的输入
            tokens.append(tok)
        return tokens

# 示例用法
if __name__ == '__main__':
    tokenizer = Lexer()
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        raise Exception("需要输入您的代码文件")
    elif len(sys.argv) > 2:
        raise Exception("您输入的文件太多了")
    else :
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            code = file.read()
        tokens = tokenizer.tokenize(code)
        for tok in tokens:
            print(tok)