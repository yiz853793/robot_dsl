# interpreter.py
import AST, parser, lexer
import os, subprocess, sys
from contextlib import contextmanager, redirect_stdout

class Interpreter:
    ''' 按照规则运行AST树 '''
    def __init__(self, code):
        self._parser = parser.Parser(lexer.Lexer())
        self.root_node = self._parser.parse(code) # AST树根节点
        self.variables = [{}]  # 存储变量及其值，模仿栈帧
        self.functions = {}  # 存储函数
        self.returned = False # 存储是否返回
    
    def run(self):
        self._execute_node(self.root_node)
    
    def _get_ASTNode_value(self, node : AST.ASTNode):
        '''获取节点的值'''
        if node.type == 'STR' or node.type == 'NUMBER' or node.type == 'TRUE' or node.type == 'FALSE':
            return node.value
        
        if node.type == 'ID':
            return self._get_ID_value(node)

        if node.type == 'array_item':
            return self._get_array_item_value(node)

        if node.type == 'array' or node.type == 'argument_list':
            return self._get_array_value(node)

        if node.type == 'factor' :
            return self._get_factor_value(node)
        
        if node.type == 'term':
            return self._get_term_value(node)

        if node.type == 'expression':
            return self._get_expression_value(node)
            
        if node.type == 'boolfactor' :
            return self._get_boolfactor_value(node)
            
        if node.type == 'boolterm':
            return self._get_boolterm_value(node)
        
        if node.type == 'boolexpression' :
            return self._get_boolexpression_value(node)
        
        if node.type == 'condition':
            return self._get_condition_value(node)
        
        if node.type == 'python_call':
            return self._execute_python_call(node)
        
        if node.type == 'function_call':
            return self._execute_function_call(node)

    def _get_ID_value(self, node : AST.ASTNode):
        '''根据ID获取一个值'''
        # 从栈顶开始查找变量
        for i in range(len(self.variables) - 1, -1, -1):
            if node.value in self.variables[i]: # 找到该变量
                return self.variables[i][node.value]
        raise Exception(f"变量 {node.value} 未赋值")

    def _get_array_item_value(self, node : AST.ASTNode):
        '''获取一个数组元素的值，第一个子节点是ID，第二个是expression表示索引'''
        # 获取索引值
        idx = self._get_ASTNode_value(node.children[0])  # 第一个子节点是索引表达式
        if not isinstance(idx, int):
            raise Exception(f"数组 {node.value} 的索引 {idx} 不是一个数字")

        # 从栈顶开始查找变量
        for i in range(len(self.variables) - 1, -1, -1):
            if node.value in self.variables[i]:  # 找到该变量
                m = self.variables[i][node.value]
                if isinstance(m, (int, float)):
                    raise Exception(f"变量 {node.value} 是一个数而不是数组")
                if len(m) <= idx or idx < 0:
                    raise Exception(f"数组 {node.value} 没有第 {idx} 项")                    
                return m[idx]
                
        raise Exception(f"没有找到变量 {node.value}")

    def _get_array_value(self, node : AST.ASTNode):
        '''获取一个数组或参数列表的值，返回值是数组，子节点都是expression'''
        ans = []
        for it in node.children:
            ans.append(self._get_ASTNode_value(it))
        return ans

    def _get_factor_value(self, node : AST.ASTNode):
        '''获取一元运算节点的值'''
        val = self._get_ASTNode_value(node.children[0])

        if node.operation == '-': # 取负值              
            if isinstance(val, (int, float)):  # 对数字类型取负
                return -val
            raise Exception(f"{val} 不是数，无法取负值")

        if node.operation == 'atoi' : # 字符转数操作
            if not isinstance(val, str):
                raise Exception(f"{val} 不是字符串, 操作符atoi出错")
            try:
                return int(val)
            except ValueError:
                try:
                    # 如果无法转为整数，尝试转换为浮点数
                    return float(val)
                except ValueError:
                    raise Exception(f"字符串 '{val}' 无法转换成数字")
        
        if node.operation == 'itoa' : # 数转字符操作
            return str(val)

    def _get_term_value(self, node : AST.ASTNode):
        '''获取乘除法的值'''
        val1 = self._get_ASTNode_value(node.children[0])
        val2 = self._get_ASTNode_value(node.children[1])
        if node.operation == '*':
            if isinstance(val1, int) or isinstance(val2, int): # 两个参数有一个是整数，可以进行乘法
                return val1 * val2
            if isinstance(val1, float) and isinstance(val2, float): # 两个参数数都是小数也能相乘
                return val1 * val2
            raise Exception(f"{val1} 和 {val2} 无法做乘法")
            
        if node.operation == '/':
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)): # 两个参数数都是数才能相除
                if val2 == 0:
                    raise Exception(f"除数不能为零 ({val1} / {val2})")
                return val1 / val2
            raise Exception(f"{val1} 和 {val2} 无法做除法")

    def _get_expression_value(self, node : AST.ASTNode):
        '''获取加减法的值'''
        val1 = self._get_ASTNode_value(node.children[0])
        val2 = self._get_ASTNode_value(node.children[1])
        if node.operation == '+':
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 + val2
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 + val2
            if isinstance(val1, list) and isinstance(val2, list):
                return val1 + val2 
            raise Exception(f"{val1} 和 {val2} 类型不一致，不能进行加法")
        if node.operation == '-':
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 - val2
            raise Exception(f"{val1} 和 {val2} 不是全数，不能进行减法")

    def _get_boolfactor_value(self, node : AST.ASTNode):
        '''获取not取反的值'''
        val = self._get_ASTNode_value(node.children[0])
        if node.operation == 'not' :
            return not val
    
    def _get_boolterm_value(self, node : AST.ASTNode):
        '''获取判断的值'''
        val1 = self._get_ASTNode_value(node.children[0])
        val2 = self._get_ASTNode_value(node.children[1])
        if node.operation == '==' :
            return val1 == val2    

        if node.operation == '!=' :
            return val1 != val2
                    
        if node.operation == '>' :
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 > val2
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 > val2
            if isinstance(val1, list) and isinstance(val2, list):
                return val1 > val2
            raise Exception(f"{val1} 和 {val2} 之间不能使用>运算符")
            
        if node.operation == '>=' :
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 >= val2
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 >= val2
            if isinstance(val1, list) and isinstance(val2, list):
                return val1 >= val2
            raise Exception(f"{val1} 和 {val2} 之间不能使用>=运算符")
            
        if node.operation == '<' :
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 < val2
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 < val2
            if isinstance(val1, list) and isinstance(val2, list):
                return val1 < val2
            raise Exception(f"{val1} 和 {val2} 之间不能使用<运算符")
            
        if node.operation == '<=' :
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                return val1 <= val2
            if isinstance(val1, str) and isinstance(val2, str):
                return val1 <= val2
            if isinstance(val1, list) and isinstance(val2, list):
                return val1 <= val2
            raise Exception(f"{val1} 和 {val2} 之间不能使用<=运算符")
    
    def _get_boolexpression_value(self, node : AST.ASTNode):
        '''获取并运算的结果'''
        for child in node.children :
            val = self._get_ASTNode_value(child)
            if not val:
                return False
        return True

    def _get_condition_value(self, node : AST.ASTNode):
        '''获取或运算的结果'''
        for child in node.children :
            val = self._get_ASTNode_value(child)
            if val:
                return True
        return False

    def _execute_node(self, node : AST.ASTNode):
        '''运行节点的操作'''
        if node.type == 'assign':
            return self._execute_assign_statement(node)
        
        if node.type == 'function_def':
            return self._execute_function_define(node)
        
        if node.type == 'program':
            return self._execute_program(node)
        
        if node.type == 'return':
            return self._execute_return(node)

        if node.type == 'python_call':
            return self._execute_python_call(node)

        if node.type == 'function_call':
            return self._execute_function_call(node)
        
        if node.type == 'if':
            return self._execute_if_statement(node)
        
        if node.type == 'while':
            return self._execute_while_statement(node)
    
    def _execute_assign_statement(self, node : AST.ASTNode):
        '''取等号操作，第一个子节点是标识符或数组元素，第二个子节点是expression'''
        var_name = node.children[0].value
        find_var = False
        # 从栈帧顶开始搜索
        for i in range(len(self.variables) - 1, -1, -1):
            if var_name in self.variables[i] :
                find_var = True
                if node.children[0].type == 'ID' :
                    self.variables[i][var_name] = self._get_ASTNode_value(node.children[1])
                if node.children[0].type == 'array_item' :
                    value = self.variables[i].get(var_name)
                    if not isinstance(value, list):
                        raise Exception(f'{var_name} 是一个变量而不是数组')
                    idx = self._get_ASTNode_value(node.children[0].children[0])
                    if not isinstance(idx, int):
                        raise Exception(f'{idx} 不是整数')
                    if idx >= len(value) or idx < 0:
                        raise Exception(f'数组 {var_name} 不包含第 {idx} 项')
                    self.variables[i][var_name][idx] = self._get_ASTNode_value(node.children[1])
        # 如果不在栈中，设为全局变量
        if not find_var:
            self.variables[0][var_name] = self._get_ASTNode_value(node.children[1])
                    

    def _execute_python_call(self, node: AST.ASTNode):
        '''调用外部python脚本，子节点argument_list为调用的参数'''
        script_path = node.operation  
        arguments = self._get_ASTNode_value(node.children[0])
        
        if not os.path.isabs(script_path):  # If the path is relative, make it absolute
            script_path = os.path.join(os.getcwd(), script_path)

        # Make sure the file exists
        if not os.path.isfile(script_path):
            raise Exception(f"Python 脚本 {script_path} 不存在")
        
        args = [str(arg) for arg in arguments]
        try:
            result = subprocess.run([sys.executable, script_path] + args, 
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip() # 脚本输出结果
        except subprocess.CalledProcessError as e:
            raise Exception(f"调用 {script_path} 脚本执行失败，错误信息:\n {e.stderr.strip()}")     

    def _execute_function_define(self, node: AST.ASTNode):
        '''函数函数声明，子节点为argument_list为函数参数，子节点的子节点应该全是ID'''
        function_name = node.operation
        if function_name == 'print' or function_name == 'input' or function_name == 'len':
            raise Exception(f'函数 {function_name} 是内置函数')

        argument_nodes = node.children[0].children
        
        argument_names = []
        
        for arg in argument_nodes:
            if arg.type != 'ID':
                raise Exception(f"函数 {function_name} 中有 {arg.type} ,希望是一个标识符")
            
            # Check for uniqueness of the argument
            if arg.value in argument_names:
                raise Exception(f"在函数 {function_name} 中，{arg.value} 重复定义")
            
            argument_names.append(arg.value)

        program_body = node.children[1]
        
        # 存储在self.functions里
        self.functions[function_name] = {
            'arguments': argument_names,
            'body': program_body,
        }
        
        return None

    def _execute_function_call(self, node: AST.ASTNode):
        '''函数调用，子节点为argument_list为函数参数，子节点的子节点都是expression'''
        function_name = node.operation

        # 内置print inut 和 len函数
        if function_name == 'print' :
            arguments = self._get_ASTNode_value(node.children[0])
            args_str = [self._handle_escape_sequences(str(arg)) for arg in arguments]
            print(''.join(args_str), end='')
            return None

        if function_name == 'input':
            arguments = self._get_ASTNode_value(node.children[0])
            args_str = [self._handle_escape_sequences(str(arg)) for arg in arguments]
            print(''.join(args_str), end='')
            return input()
        
        if function_name == 'len':
            arguments = self._get_ASTNode_value(node.children[0])
            ans = []
            for arg in arguments:
                if isinstance(arg, (list, str)):
                    ans.append(len(arg))
                else :
                    ans.append(None)
            return ans

        if function_name not in self.functions:
            raise Exception(f'{function_name} 未定义，无法调用')
        
        arguments = self._get_ASTNode_value(node.children[0])  # Arguments from the function call
        
        function_tuple = self.functions[function_name]
        defined_arguments = function_tuple['arguments']

        if len(arguments) != len(defined_arguments):
            raise Exception(f"{function_name} 函数的参数不匹配")

        # 设置栈帧
        self.variables.append({})

        for arg_name, arg_value in zip(defined_arguments, arguments):
            self.variables[-1][arg_name] = arg_value  # Bind each argument to its value in the current scope

        return_value = None
        self.returned = False

        try:
            return_value = self._execute_node(function_tuple['body'])
        except Exception:
            raise Exception(f"函数 {function_name} 运行中出错")
        finally:
            # 弹出栈帧
            self.variables.pop()
        
        # 将是否返回改为否
        self.returned = False
        return return_value

    def _execute_program(self, node : AST.ASTNode):
        '''执行一段程序，子节点分别是一个个语句'''
        ans = None
        self.returned = False
        for child_node in node.children :
            if not self.returned:
                # program中可能有return语句，return后不再执行后面的语句
                ans = self._execute_node(child_node)
        
        # 如果有return语句，将return值返回给父节点
        if self.returned:
            return ans
        return None

    def _execute_return(self, node : AST.ASTNode):
        '''执行返回语句，第一个子节点是返回值'''
        return_value = None
        if node.children : 
            return_value = self._get_ASTNode_value(node.children[0])
        # 将是否返回改为是
        self.returned = True
        return return_value

    def _execute_if_statement(self, node : AST.ASTNode) :
        '''执行if语句，第一个是判断条件condition，第二、三个都是program，为真执行第二个，否执行第三个'''
        condition_var = self._get_ASTNode_value(node.children[0])
        self.returned = False
        return_value = None
        if condition_var :
            return_value = self._execute_node(node.children[1])
        elif len(node.children) == 3:
            return_value = self._execute_node(node.children[2])
        
        if self.returned:
            return return_value
        return None

    def _execute_while_statement(self, node : AST.ASTNode):
        '''执行while语句，第一个是判断条件condition，第二是program，为真执行第二个'''
        condition_var = self._get_ASTNode_value(node.children[0])
        self.returned = False
        return_value = None
        while condition_var :
            return_value = self._execute_node(node.children[1])
            if self.returned : 
                break
            condition_var = self._get_ASTNode_value(node.children[0])
        
        if self.returned :
            return return_value
        return None

    def _handle_escape_sequences(self, text: str):
        """处理字符串中的转义字符"""
        ans = ''
        escape = False
        for ch in text:
            if escape:
                if ch == 'n':
                    ans+='\n'
                elif ch == 't':
                    ans += '\t'
                elif ch == '\'':
                    ans += '\''
                elif ch == '\"':
                    ans += '\"'
                elif ch == '\\':
                    ans += '\\'
                escape = False
            else :
                if ch == '\\':
                    escape = True
                else : 
                    ans += ch
        return ans
    
# 测试解释器
if __name__ == "__main__":
    with open('scripts\\a.dsl', 'r', encoding='utf-8') as f:
        code = f.read()

    interpreter = Interpreter(code)
    interpreter.run()

