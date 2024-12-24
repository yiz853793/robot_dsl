# 测试更复杂的 if 语句和 while 循环

x = 10
y = 0
z = 5

if x > 5 and z < 10 begin
    y = x * z
    if y > 40 begin
        y = y - 10
    else
        y = y + 10
    end
else
    y = y + 5
end

print(y, '\n')

while y < 100 begin
    y = y + 15
    if y == 70 begin
        y = y + 30
    end
end

print(y, '\n')
