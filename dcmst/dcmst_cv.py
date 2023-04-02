import random
import networkx as nx
import numpy as np

from utils_cv import *
# from utils import compute_degree
from utils import *


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


def convert_lset_to_llist(lset):
    llist = [list(item) for item in lset]
    return llist


def make_graph_connected(G):
    # Tìm các thành phần liên thông của đồ thị
    subgraphs = list(nx.connected_components(G))
    subgraphs = convert_lset_to_llist(subgraphs)
    # print(subgraphs)

    # Nếu đồ thị đã liên thông, không cần thực hiện gì thêm
    if len(subgraphs) == 1:
        return G

    # Thêm các cạnh để kết nối các thành phần liên thông
    for i in range(len(subgraphs) - 1):
        nodes1 = subgraphs[i]
        nodes2 = subgraphs[i + 1]
        node1 = nodes1[0]
        node2 = nodes2[0]
        G.add_edge(node1, node2)

    return G


def fix_cycle(nx_graph):
    """Đầu vào là một đồ thị liên thông"""
    while is_cycle(nx_graph):
        c = nx.find_cycle(nx_graph)
        nx_graph.remove_edge(c[1][0], c[1][1])
    return nx_graph


def is_cycle(nx_graph):
    if not nx.is_tree(nx_graph) and nx.is_connected(nx_graph):
        return True
    else:
        return False


def repair_degree(degree_constrained, G):
    # Tạo đồ thị cây từ danh sách cạnh
    # G = nx.Graph(edges)
    subgraphs = []
    # Kiểm tra giới hạn bậc của mỗi đỉnh
    for v in G.nodes():
        if G.degree(v) > degree_constrained:
            # Nếu có đỉnh có giới hạn bậc quá n, thực hiện sửa cây
            # Tìm các đỉnh kề của đỉnh này
            neighbors = list(G.neighbors(v))
            # print("v, neighbor", v, neighbors)
            # Xóa các cạnh kết nối đỉnh này với các đỉnh kề
            for i in range(len(neighbors) - degree_constrained):
                G.remove_edge(neighbors[i], v)

            subgraphs = list(nx.connected_components(G))
    subgraphs = convert_lset_to_llist(subgraphs)
    # print(subgraphs)
    degree = compute_degree(G)
    # print(degree)
    subgraphs = sort_sublists(subgraphs, degree)
    # print(subgraphs)
    while len(subgraphs) > 1:
        # Ghép 2 đồ thị đầu tiên
        G.add_edge(subgraphs[0][0], subgraphs[1][0])
        # Tính toán lại subgraph và bậc đồ thị sau khi ghép
        subgraphs = list(nx.connected_components(G))
        subgraphs = convert_lset_to_llist(subgraphs)
        degree = compute_degree(G)
        subgraphs = sort_sublists(subgraphs, degree)
        # print(subgraphs)

    # Trả về danh sách cạnh của cây đã được sửa
    return G


def repair_pop(pop, degree_constrained):
    for i in range(len(pop)):
        # print("individual", i)
        n = compute_n(len(pop[i]))
        print(n)
        edges = decode_to_graph(n, pop[i])
        print(edges)
        # print(edges)
        # Làm đồ thị liên thông
        G = nx.empty_graph(n)
        G = G.add_edges_from(edges)
        G = make_graph_connected(G)
        # print(G.edges())
        # Xóa chu trình
        G = fix_cycle(G)
        # print(is_cycle(G))
        G = repair_degree(degree_constrained, G.edges())
        pop[i] = encode_to_cv(n, G.edges())
    return pop


# edges = [(0, 1), (2, 3), (2, 4), (2, 5), (6, 7), (7, 8), (8, 6), (7, 2), (4, 8)]
# edges = [(0, 1)]
# n = 5
# # # bit = gen_bit(n)
# bit = [0, 1, 0, 0, 1, 0, 0, 1, 1, 1]
# print(bit)
# edges = decode_to_graph(n, bit)
# print("Tree: ", edges)
#
# G = nx.empty_graph(n)
# G.add_edges_from(edges)
# G = make_graph_connected(G)
# print("Connect: ", G.edges)
#
# print("Fix Cycle", fix_cycle(G).edges())
# repair_degree(2, G)
# print("Out: ", G.edges())
# print(nx.is_tree(G))

pop = [[0, 0, 0, 0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 0, 1, 1, 1]]
repair_pop(pop, 2)
print(pop)