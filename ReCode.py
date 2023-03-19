#! python3
# ReCode.py

import re
# pattern = re.compile(r'''[a-zA-Z][\s\w]+\s+ # 必须从字母开始
#     ([\w]+)   # 函数名
#     \([\s\w]*\) # 函数入参
#     \s*\{([\s\S]*?)\}''') # 函数体，非贪婪匹配
# 正则表达式可视化 https://c.runoob.com/front-end/7625/#!flags=&re=


pattern = re.compile(r'''[a-zA-Z][\s\w]+\s+([\w]+)\([\s\w]*\)\s*\{([\s\S]*?)\}''')
with open('TestText.txt', 'r') as f:
    str = f.read()

print(pattern.search(str).group(0))

for g in pattern.findall(str) :
    print(g)
