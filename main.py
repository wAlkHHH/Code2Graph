#! python3
import matplotlib.pyplot as plt
import networkx as nx
import openpyxl as pxl
import os
import pickle
import datetime


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
                

        


        
            
graph = {}
G = nx.DiGraph()

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
    print("开始构建......")
    options = {
        "font_size": 36,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    for layer, nodes in enumerate(nx.topological_generations(G)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer
    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(G, subset_key="layer")

    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, ax=ax, **options)
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    plt.show()
    print("构建完成......")
    saveFile = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(saveFile, "wb") as f :
        pickle.dump(graph, f)