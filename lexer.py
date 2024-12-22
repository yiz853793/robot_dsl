# lexer.py
import ply.lex as lex

class Lexer:
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
        # 'SEMICOLON',
        'COMMA',
        'NUMBER',
        'ID',
        'STR',
        'CALLPY',
    ] + list(reserved.values())

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
    # t_SEMICOLON     = r';'
    t_COMMA         = r','


    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'\d+(\.\d*)?'
        t.value = {'value' : int(t.value), 'type' : 'NUMBER'}
        return t
    
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

    def t_STR(self, t):
        r'''("((\\\")|[^\n\"])*")|('((\\\')|[^\n\'])*')'''
        t.value = {'value' : t.value[1:-1], 'type' : 'STR'}
        return t

    def t_CALLPY(self, t):
        r'./([a-zA-Z]:\\)?([0-9a-zA-Z_]+\\)*[0-9a-zA-Z_]+.py'
        t.value = {'value' : t.value[2:], 'type' : 'CALLPY'}
        return t
    
    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character {t.value} in line {t.lexer.lineno}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)  # Build the lexer

    def tokenize(self, data):
        """Take the input data and tokenize it."""
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            tokens.append(tok)
        return tokens

# Example usage
if __name__ == '__main__':
    with open('scripts\\a.dsl', 'r', encoding='utf-8') as f:
        data = f.read()
    # print(data)
    tokenizer = Lexer()
    tokens = tokenizer.tokenize(data)
    
    for tok in tokens:
        print(tok)