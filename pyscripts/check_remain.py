import sys

if __name__ == '__main__':
    remain = {'张三' : 100, '李四' : 200, '王五' : 300}
    if len(sys.argv) >= 2 :
        name = sys.argv[1]
        if name in remain :
            print( remain[name] )