function add(a, b)
begin
    return a + b
end
a = '你好' b = '世界'
print(add(a, b), '\n')

while a != 'end' begin
    a = input('请输入，我会重复您的话：')
    print(a, '\n')
end
