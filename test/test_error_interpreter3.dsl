# 测试解释器函数调用参数不匹配

function add(a, b) begin
    return a + b
end

result = add(5)  # 缺少一个参数
print(result)
