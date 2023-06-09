#! python3
import matplotlib.pyplot as plt
import networkx as nx
import openpyxl as pxl
import os
import pickle
import datetime
from pyvis import network as vis_net
import networkx as nx
import ReCode

tab_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
graph = {}
G = nx.DiGraph()

def inputMode():
    while True :
        print("输入起始点，以空格分隔，第一个参数为起点，或者输入end结束")
        str = input()
        nodes = str.split(" ")
        n = len(nodes)
        if n == 0 :
            continue
        elif n == 1 :
            if str.lower().startswith("end") :
                break
            else :
                continue
        G.add_node(nodes[0])
        graph.setdefault(nodes[0], set())
        for i in range(1, len(nodes)) :
            G.add_edge(nodes[0], nodes[i])
            graph[nodes[0]].add(nodes[i])

def fileMode():
    while True :
        print("输入pickle文件的路径或者输入end结束")
        str = input()
        if str.lower().startswith("end") :
            break

        str = os.path.abspath(str)
        if not os.path.exists(str) :
            print("文件不存在")
            continue
        with open(str, "rb") as f :
            oldGraph = pickle.load(f)
        if not isinstance(oldGraph, dict) :
            print("文件类型错误")
            continue
        
        for start, ends in oldGraph :
            G.add_node(start)
            graph.setdefault(start, set())
            for node in ends :
                G.add_edge(start, node)
                graph[start].add(node)

def transferDiyG2NxG():
    for start, ends in graph.items() :
        G.add_node(start)
        for node in ends :
            G.add_edge(start, node)
            graph[start].add(node)

def walkDirAndProcCode(absPath):
    for folderName, subfolders, filenames in os.walk(absPath) :
            for filename in filenames :
                if not filename.lower().endswith(".c") :
                    continue
                with open(os.path.join(folderName, filename), "r") as f :
                    codeText = f.read()
                    ReCode.ProcCodeText2Graph(codeText, graph)
            for subfolder in subfolders :
                walkDirAndProcCode(os.path.join(folderName, subfolder))


def dirMode():
    while True :
        print("输入代码目录路径或者输入end结束")
        str = input()
        if str.lower().startswith("end") :
            break
        # str = os.path.abspath(str)
        if not os.path.exists(str) :
            print("文件不存在")
            continue
        if str.endswith(".c") :
            print("路径非目录")
            continue
        walkDirAndProcCode(str)
    transferDiyG2NxG()
    
if __name__ ==  "__main__":
    pos = {}
    cnt = 0;
    while True :
        print("选择不同的模式，或者输入end结束,输入quit直接退出")
        str = input()
        if str.lower().startswith("end") :
            break
        elif str.lower().startswith("quit") :
            print("退出...")
            exit(0)
        elif str.lower().startswith("i") :
            inputMode()
        elif str.lower().startswith("e") :
            fileMode()
        elif str.lower().startswith("dir") :
            dirMode()
    print("开始构建......")
    colors_of_node = nx.coloring.greedy_color(G)
    print(colors_of_node)
    for node in list(G.nodes) :
        # G.nodes[node]['color'] = colors_of_node[node]
        G.nodes[node]['color'] = tab_colors[colors_of_node[node]%len(tab_colors)]
        # print(G.nodes[node]['color'])
    # print(list(G.nodes(data='color', default=None)))
    nt = vis_net.Network("500px", "1000px", directed=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics', 'nodes', 'selection', 'layout'])

    # TO DO -- check if the file is exited
    nt.show("nx.html", notebook=False)
    print("构建完成......")
    # TO DO -- save the files in other ways including the graph file
    # saveFile = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # with open(saveFile, "wb") as f :
    #     pickle.dump(graph, f)