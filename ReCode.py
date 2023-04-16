#! python3
# ReCode.py

import re
from pyvis import network as vis_net
import networkx as nx
# pattern = re.compile(r'''[a-zA-Z][\s\w]+\s+ # 必须从字母开始
#     ([\w]+)   # 函数名
#     \([\s\w]*\) # 函数入参
#     \s*\{([\s\S]*?)\}''') # 函数体，非贪婪匹配
# 正则表达式可视化 https://c.runoob.com/front-end/7625/#!flags=&re=

def ProcCodeText2Graph(codeText, codeGraph) :
    pattern = re.compile(r'''[a-zA-Z][\s\w]+\s+([\w]+)\([\s\w*]*\)\s*\{([\s\S]*?)\}''')
    pattern_for_func = re.compile(r'''([\w]+)\([\W\w]*?\)''')
    # with open('TestText.txt', 'r') as f:
    #     codeText = f.read()

    # print(pattern.search(str).group(0))
    # codeGraph = dict()
    for g in pattern.findall(codeText) :
        print(g)
        codeGraph.setdefault(g[0], set())
        for func in pattern_for_func.findall(g[1]) :
            print(func)
            codeGraph[g[0]].add(func)
    return codeGraph

if __name__ ==  "__main__":

    G = nx.DiGraph()
    codeGraph = dict()
    for src, dsts in codeGraph.items() :
        G.add_node(src)
        print("src: %s"%src)
        for dst in dsts :
            G.add_edge(src, dst)
            print("dst: %s"%dst)
    nt = vis_net.Network("500px", "1500px", directed=True)
    nt = vis_net.Network("500px", "1500px", directed=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics'])
    # TO DO -- check if the file is exited
    nt.show("nx.html", notebook=False)
    print("构建完成......")
