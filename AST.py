# AST.py
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