import math

import networkx as nx


def encode_to_cv(n, edges):
    """mã hóa đồ thị n đỉnh thành chuỗi bit"""
    g = nx.complete_graph(n)
    g_edges = list(g.edges)

    bit = [0] * len(g_edges)
    for i in range(len(g_edges)):
        if g_edges[i] in edges:
            bit[i] = 1
    return bit


def decode_to_graph(n, cv):
    g = nx.complete_graph(n)
    g_edges = list(g.edges)
    edges = []
    for i in range(len(g_edges)):
        if cv[i] == 1:
            edges.append(g_edges[i])
    return edges


def make_graph_connected(G):
    """Biến đồ thị không liên thông trở thành liên thông"""
    # Tìm các thành phần liên thông của đồ thị
    subgraphs = list(nx.connected_components(G))
    # print(subgraphs)

    # Nếu đồ thị đã liên thông, không cần thực hiện gì thêm
    if len(subgraphs) == 1:
        return G

    # Thêm các cạnh để kết nối các thành phần liên thông
    for i in range(len(subgraphs) - 1):
        nodes1 = subgraphs[i]
        nodes2 = subgraphs[i + 1]
        node1 = nodes1.pop()
        node2 = nodes2.pop()
        G.add_edge(node1, node2)

    return G


def fix_cycle(nx_graph):
    """Đầu vào là một đồ thị liên thông"""
    while is_cycle(nx_graph):
        c = nx.find_cycle(nx_graph)
        nx_graph.remove_edge(c[1][0], c[1][1])
    return nx_graph


# def is_cycle(nx_graph):
#     if not nx.is_tree(nx_graph) and nx.is_connected(nx_graph):
#         return True
#     else:
#         return False


def compute_n(len):
    delta = 1 + 8 * len
    sqrt_delta = math.sqrt(delta)
    n = int((1 + sqrt_delta) / 2)
    return n


def is_cycle(G):
    try:
        if nx.find_cycle(G):
            return True
        else:
            return False
    except:
        return False


G = nx.complete_graph(4)
T = nx.empty_graph(4)
T.add_edges_from([(2, 4), (2, 3)])
# print(is_cyc(T))
