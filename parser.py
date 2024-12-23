# parser.py
import ply.yacc as yacc
import lexer
import AST
import sys

class ParserError(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.message)

    def __str__(self):
        if self.token:
            return f"Error at token {self.token.type} ({self.token.value}): {self.message}"
        return f"Error: {self.message}"

class Parser:
    '''
    <program> ::= <program> <statement>
           | <empty>

    <statement> ::= <assign>
                | <if_state>
                | <while_state>
                | <python_call>
                | <function_call>
                | <function_def>
                | <return_statement>

    <python_call> ::= CALLPY '(' <argument_lists> ')'

    <assign> ::= ID = <expression>
            | <array_item> = <expression>

    <if_state> ::= IF <condition> BEGIN <program> END
                | IF <condition> BEGIN <program> ELSE <program> END

    <function_def> ::= FUNCTION ID '(' <argument_lists> ')' BEGIN <program> END

    <function_call> ::= ID '(' <argument_lists> ')'

    <return_statement> ::= RETURN
                    | RETURN <condition>

    <condition> ::= <condition> OR <boolexpression>
                | <boolexpression>

    <boolexpression> ::= <boolexpression> AND <boolterm>
                    | <boolterm>

    <boolterm> ::= <boolfactor>
            | <boolterm> '==' <boolfactor>
            | <boolterm> '!=' <boolfactor>
            | <boolterm> '<=' <boolfactor>
            | <boolterm> '<' <boolfactor>
            | <boolterm> '>=' <boolfactor>
            | <boolterm> '>' <boolfactor>

    <boolfactor> ::= NOT <boolfactor>
                | <expression>

    <expression> ::= <expression> '+' <term>
                | <expression> '-' <term>
                | <term>

    <term> ::= <term> '*' <factor>
            | <term> '/' <factor>
            | <factor>

    <factor> ::= '(' <condition> ')'
            | - <factor>
            | '(atoi)' <factor>
            | '(itoa)' <factor>
            | NUMBER
            | STR
            | ID
            | <array_item>
            | <array>
            | <python_call>
            | TRUE
            | FALSE
            | <function_call>

    <array> ::= '[' <argument_lists> ']'

    <array_item> ::= ID '[' <expression> ']'

    <argument_lists> ::= <argument_list>
                    | <empty>

    <argument_list> ::= <expression>
                    | <argument_list> COMMA <expression>

    <empty> ::= 
    '''
    def __init__(self, Lexer: lexer.Lexer):
        self._lexer = Lexer
        self.tokens = Lexer.tokens
        self._yacc = yacc.yacc(module=self, debug=True, method='LALR')

    def _p_ASTNode(self, node):
        """用p构造ASTNode"""
        if isinstance(node, AST.ASTNode):
            return node
        else:
            return AST.ASTNode(type=node['type'], value=node['value'])

    def _create_children(self, *child_list):
        """构造ASTNode的数组"""
        root_children = []
        for child in child_list:
            root_children.append(self._p_ASTNode(child))
        return root_children

    def p_program(self, p):
        '''
            program : program statement
                   | 
        '''
        if len(p) == 3:
            p[0] = p[1]
            p[0].add_child(p[2])
        else:
            p[0] = AST.ASTNode(type='program')

    def p_statement(self, p):
        '''
            statement : assign
                     | if_state
                     | while_state
                     | python_call
                     | function_call
                     | function_def
                     | return_statement
        '''
        p[0] = p[1]
        
    def p_python_call(self, p):
        '''
            python_call : CALLPY LPAREN argument_lists RPAREN
        '''
        p[0] = AST.ASTNode(type = 'python_call', operation = p[1]['value'], 
                           children=self._create_children(p[3]))
        
    def p_assign(self, p):
        """
            assign : ID ASSIGNMENT expression
                  | array_item ASSIGNMENT expression
        """
        if len(p) == 4:
            p[0] = AST.ASTNode(type='assign', operation=p[2],
                               children=self._create_children(p[1], p[3]))

    def p_if_state(self, p):
        '''
            if_state : IF condition BEGIN program END
                    | IF condition BEGIN program ELSE program END
        '''
        if len(p) == 6:
            p[0] = AST.ASTNode(type='if', children=self._create_children(p[2], p[4]))
        else:
            p[0] = AST.ASTNode(type='if', children=self._create_children(p[2], p[4], p[6]))

    def p_while_state(self, p):
        '''while_state : WHILE condition BEGIN program END'''
        p[0] = AST.ASTNode(type='while', children=self._create_children(p[2], p[4]))

    def p_function_def(self, p):
        '''
            function_def : FUNCTION ID LPAREN argument_lists RPAREN BEGIN program END
        '''
        p[0] = AST.ASTNode(type='function_def', operation=p[2]['value'],
                           children=self._create_children(p[4], p[7]))

    def p_function_call(self, p):
        '''
            function_call : ID LPAREN argument_lists RPAREN
        '''
        p[0] = AST.ASTNode(type='function_call', operation=p[1]['value'],
                           children=self._create_children(p[3]))

    def p_return_statement(self, p):
        '''
            return_statement : RETURN
                              | RETURN condition
        '''
        if len(p) == 2:
            p[0] = AST.ASTNode(type='return')
        else:
            p[0] = AST.ASTNode(type='return', children=self._create_children(p[2]))

    def p_condition(self, p):
        '''    
            condition ::= condition OR boolexpression
                        | boolexpression
        '''
        if len(p) == 4:
            if p[1].type == 'condition':
                p[0] = p[1]
                p[0].add_child(self._p_ASTNode(p[3]))
            else :
                p[0] = AST.ASTNode(type='condition', operation=p[2],
                                   children=self._create_children(p[1], p[3]))
        else :
            p[0] = p[1]

    def p_boolexpression(self, p):
        """
            boolexpression : boolexpression AND boolterm
                            | boolterm
        """
        if len(p) == 4:
            if p[1].type == 'boolexpression':
                p[0] = p[1]
                p[0].add_child(self._p_ASTNode(p[3]))
            else :
                p[0] = AST.ASTNode(type='boolexpression', operation=p[2],
                                   children=self._create_children(p[1], p[3]))
        else :
            p[0] = p[1]
    
    def p_boolterm(self, p):
        """
            boolterm : boolfactor
                      | boolterm EQUAL boolfactor
                      | boolterm NEQ boolfactor
                      | boolterm LEQ boolfactor
                      | boolterm LSS boolfactor
                      | boolterm GEQ boolfactor
                      | boolterm GTR boolfactor
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.ASTNode(type = 'boolterm', operation=p[2], 
                               children=self._create_children(p[1], p[3]))
    def p_boolfactor(self, p):
        '''
            boolfactor :  NOT boolfactor
                        | expression
        '''
        if len(p) == 2 :
            p[0] = p[1]
        else:
            p[0] = AST.ASTNode(type='boolfactor', operation=p[1], 
                               children=self._create_children(p[2]))

    def p_expression(self, p):
        """
            expression : expression PLUS term
                        | expression MINUS term
                        | term
        """
        if len(p) == 4:
            p[0] = AST.ASTNode(type='expression', operation=p[2], 
                               children=self._create_children(p[1], p[3]))
        else:
            p[0] = p[1]

    def p_term(self, p):
        """
            term : term TIMES factor
                | term DIVIDE factor
                | factor
        """
        if len(p) == 4:
            p[0] = AST.ASTNode(type='term', operation=p[2], 
                               children=self._create_children(p[1], p[3]))
        else:
            p[0] = p[1]
    def p_factor(self, p):
        """
            factor : LPAREN condition RPAREN
                  | MINUS factor
                  | LPAREN ATOI RPAREN factor
                  | LPAREN ITOA RPAREN factor
                  | NUMBER
                  | STR
                  | ID
                  | array_item
                  | array
                  | python_call
                  | TRUE
                  | FALSE
                  | function_call
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3 : # factor -> -factor
            p[0] = AST.ASTNode(type='factor', operation=p[1],
                               children=self._create_children(p[2]))
        elif len(p) == 4: # factor -> (atoi)factor | (itoa)factor
            p[0] = p[2]
        elif len(p) == 5 : # factor -> (itoa)factor | (atoi)factor
            p[0] = AST.ASTNode(type='factor', operation=p[2],
                               children=self._create_children(p[4]))
            
    def p_array_item(self, p):
        '''
            array_item : ID LBRACKET expression RBRACKET
        '''
        p[0] = AST.ASTNode(type='array_item', value=p[1]['value'], children=self._create_children(p[3]))

    def p_array(self, p) :
        '''
            array : LBRACKET argument_lists RBRACKET
        '''
        p[0] = AST.ASTNode(type='array', children=self._create_children(p[2]))
    
    def p_argument_lists(self, p):
        """
            argument_lists : argument_list 
                            |
        """
        if len(p) == 2:
            # 有一个表达式的参数列表
            p[0] = p[1]
        else:
            # 空的参数列表
            p[0] = AST.ASTNode('argument_list')

    def p_argument_list(self, p):
        """
            argument_list : expression
                        | argument_list COMMA expression
        """
        if len(p) == 2:
            # 单个表达式，表示参数列表的开始
            p[0] = AST.ASTNode('argument_list')
            p[0].add_child(self._p_ASTNode(p[1]))  # 将表达式作为子节点
        else:
            # 多个表达式，递归地处理逗号分隔的表达式
            p[0] = p[1]
            p[0].add_child(self._p_ASTNode(p[3]))  # 将逗号后的表达式作为子节点

    def p_error(self, p):
        if p:
            # 当语法错误发生时，打印详细的错误信息
            error_msg = f"Syntax error at '{p.value}' (line {p.lineno}, position {p.lexpos})"
            raise ParserError(error_msg, p)
        else:
            # 没有匹配的部分，可能是文件的结束或空的输入
            error_msg = "Syntax error at the end of the input"
            raise ParserError(error_msg)
        
    def parse(self, code : str):
        '''对目标文件进行语法分析，返回AST数的根节点'''
        return self._yacc.parse(code, lexer=self._lexer.lexer)
        
# 示例用法
if __name__ == '__main__':
    parser = Parser(lexer.Lexer())
    
    if len(sys.argv) < 2:
        raise Exception("需要输入您的代码文件")
    elif len(sys.argv) > 2:
        raise Exception("您输入的文件太多了")
    else :
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            code = file.read()
    # code = input()
        result = parser.parse(code)
        result.print()