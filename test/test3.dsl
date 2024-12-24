# 测试更复杂的函数定义与调用，以及调用外部 Python 脚本

function multiply(a, b) begin
    return a * b
end

function fibonacci(n) begin
    if n <= 0 begin
        return 0
    else
        if n == 1 begin
            return 1
        else
            return fibonacci(n - 1) + fibonacci(n - 2)
        end
    end
end

function greet(name) begin
    message = "Hello, " + name + "!"
    return message
end

x = 6
y = multiply(x, 7)
print(y)

z = fibonacci(10)
print(z)

greeting = greet("Alice")
print(greeting)

# 调用外部 Python 脚本
result = ./pyscripts\check_remain.py (z)
print(result)
