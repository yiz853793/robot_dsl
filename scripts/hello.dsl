    # scripts/hello.dsl
    print("Hello ","DSL Interpreter!\n") 
    # 输出Hello, DSL Interpreter!
    name = input('请问您的姓名：\n')
    print('您好' + name + '\n')
    a = len(name)
    a = a[0]
    print('您的名字有 ', a,' 个字\n')