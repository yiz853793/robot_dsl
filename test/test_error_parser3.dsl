# 测试解析器函数调用缺少括号

function add(a, b) begin
    return a + b
end

result = add 5, 3
print(result)
