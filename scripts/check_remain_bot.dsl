name = input('请问您的姓名，输入\'退出\'退出：')

while name != '退出' begin
    remain = ./pyscripts\check_remain.py(name)

    if remain 
    begin
        print('您的余额为', remain, '\n')
        if (atoi)remain < 200 begin
            print('您的余额少于200\n')
        end
    else
        print('对不起，没有查到您的余额。\n')
    end

    name = input('请问您的姓名，输入\'退出\'退出：')
end

function add(a, b)
begin
    return a + b
end
a = '你好' b = '世界'

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
end

a = (atoi)input("请输入一个数：") b = (atoi)input("请输入一个数：")

if cmp(a, b) begin
    print('第一个数更大\n')
else
    print('第一个数不大于第二个数\n')
end