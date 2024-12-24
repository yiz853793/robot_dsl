# 测试解析器缺少 end 关键字

x = 10
y = 20
if x > y begin
    z = x + y
# 缺少 end 关键字
print(z)
