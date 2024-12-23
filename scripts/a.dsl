function main()
begin
    print('main')
end

main()

function add(a, b)
begin
    return a + b
end
a = '你好' b = '世界\\'

function cmp(a, b) begin
    if a > b begin
        return true
    else
        return false
    end
end

print(add(a, b), '\n')

while a != 'end' begin
    a = input('请输入，我会重复您的话：')
    print(a, '\n')
    len = len(a)
    len = len[0]
    print('您输入了', len, '个字符\n')
end

a = (atoi)input("请输入一个数：") b = (atoi)input("请输入一个数：")

if cmp(a, b) begin
    print('第一个数更大')
else
    print('第一个数不大于第二个数')
end

