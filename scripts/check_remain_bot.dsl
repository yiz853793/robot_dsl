# scripts\check_remain_bot.dsl
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