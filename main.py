import interpreter
import sys

def main():
    if len(sys.argv) < 2:
        raise Exception("需要输入您的代码文件")
    elif len(sys.argv) > 2:
        raise Exception("您输入的文件太多了")
    else :
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            code = file.read()
        Interpreter = interpreter.Interpreter(code)
        Interpreter.run()

if __name__ == '__main__':
    main()
