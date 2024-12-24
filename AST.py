# AST.py
import re, sys
class ASTNode:
    def __init__(self,type:str, value=None, operation=None, children=None):
        '''
            para type:      该节点的类型，比如if_state、while_state、assign等
            para value:     该节点运行结束后的值，布尔值、数、数组和字符串
            para operation: 该节点可能执行的操作，如+、-、and、or、not等
            para children:  该节点的子节点，即该节点运行时需要运行的子代码
        '''
        self.type = type
        self.value = value  
        self.operation = operation 
        self.children = children if children is not None else [] 

    def add_child(self, child):
        """向节点添加一个子节点"""
        self.children.append(child)
    
    def __repr__(self):
        return f"({self.type}, {self.value}, {self.operation})"
    
    def set_value(self, value):
        """ 设置节点值 """
        self.value = value

    def print(self, depth = 0):
        """
        递归打印节点与子节点

        :param depth int: 深度值（默认为0）
        :raises RuntimeError: 子节点类型不为ASTNode
        """
        print('  ' * depth, end = '')
        NodeStr = str(self)
        print(NodeStr)
        for child in self.children:
            if not isinstance(child, ASTNode):
                raise RuntimeError(child)
            child.print(depth = depth + 1)

def parse_node_line(line: str):
    """
    解析单行节点字符串，返回(type, value, operation)的元组

    :param line: 字符串，如"(if_state, None, None)"
    :return: tuple(type, value, operation)
    """
    # 使用正则表达式提取括号内的内容
    match = re.match(r'\((.*?),\s*(.*?),\s*(.*?)\)', line.strip())
    if not match:
        raise ValueError(f"Invalid node format: {line}")
    
    type_str, value_str, operation_str = match.groups()

    # 解析value和operation，处理None和可能的字符串
    def parse_value(s):
        s = s.strip()
        if s == 'None':
            return None
        elif s.startswith("'") and s.endswith("'") or s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        elif re.match(r'^-?\d+(\.\d+)?$', s):
            # 数字
            if '.' in s:
                return float(s)
            else:
                return int(s)
        elif s in ('True', 'False'):
            return s == 'True'
        else:
            return s  # 其他情况作为字符串处理

    value = parse_value(value_str)
    operation = parse_value(operation_str)

    return type_str, value, operation

def reconstruct_ast_from_file(code: str) -> ASTNode:
    """
    从文件中读取AST的字符串表示并重构AST树

    :param filename: AST字符串文件路径
    :return: AST根节点
    """    
    code = code.split('\n')
    stack = []  # 栈中存储 (depth, ASTNode)
    root = None

    for line in code:
        if not line.strip():
            continue  # 跳过空行

        # 计算当前行的深度（假设每个深度使用两个空格缩进）
        leading_spaces = len(line) - len(line.lstrip(' '))
        depth = leading_spaces // 2

        # 解析节点信息
        type_str, value, operation = parse_node_line(line)
        node = ASTNode(type_str, value, operation)

        if depth == 0:
            # 根节点
            root = node
            stack = [(depth, node)]
        else:
            # 找到父节点
            while stack and stack[-1][0] >= depth:
                stack.pop()
            if not stack:
                raise ValueError(f"Invalid indentation at line: {line}")
            parent_node = stack[-1][1]
            parent_node.add_child(node)
            stack.append((depth, node))
    
    return root

# 示例用法
if __name__ == "__main__":
    sys.argv += ['test_out\\test_parser1.out']
    if len(sys.argv) < 2:
        raise Exception("需要输入您的代码文件")
    elif len(sys.argv) > 2:
        raise Exception("您输入的文件太多了")
    else :
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            code = file.read()
        root = reconstruct_ast_from_file(code)
        root.print()