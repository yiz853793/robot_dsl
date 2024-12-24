# external_script.py
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: external_script.py <number>")
        sys.exit(1)
    try:
        num = int(sys.argv[1])
        result = num * num  # 计算平方
        print(result)
    except ValueError:
        print("Invalid input")
        sys.exit(1)

if __name__ == "__main__":
    main()
