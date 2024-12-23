import subprocess
import sys

try:
    # 使用 Popen 来启动子进程并捕获输出
    result = subprocess.Popen(
        ["C:\Users\XYZ\Desktop\client\dsl\pyscripts\check_remain.py", "张三"], 
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获标准错误
        text=True,  # 返回文本而不是字节
        check=True  # 如果子进程返回非零退出码，会抛出 CalledProcessError 异常
    )
    
    # 获取子进程的输出
    ans, err = result.communicate()

    # 打印和返回结果
    print(ans)

except subprocess.CalledProcessError as e:
    raise Exception("error")
