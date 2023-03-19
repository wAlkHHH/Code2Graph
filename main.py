#! python3
import matplotlib.pyplot as plt
import networkx as nx

left, right, bottom, top, layer_sizes = .1, .9, .1, .9, [4, 7, 7, 2]
# 网络离上下左右的距离
# layter_sizes可以自己调整

if __name__ ==  "__main__":
    G = nx.DiGraph()
    pos = {}
    cnt = 0;
    while True :
        print("输入起始点，以空格分隔，第一个参数为起点，或者输入end结束,输入quit直接退出")
        str = input()
        nodes = str.split(" ")
        n = len(nodes)
        if n == 0 :
            continue
        elif n == 1 :
            if str.lower().startswith("end") :
                print("开始构建图......")
                break
            elif str.lower().startswith("quit") :
                print("退出...")
                exit(0)
            else :
                continue
        G.add_node(nodes[0])
        pos[nodes[0]] = (cnt, cnt*cnt/2)
        for i in range(1, len(nodes)) :
            G.add_edge(nodes[0], nodes[i])

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
