import networkx as nx

from utils_cv import *
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


def compute_degree(G):
    degree = {}
    nodes = G.nodes
    for i in nodes:
        degree[i] = G.degree(i)
    return degree


def sort_sublists(lst, dictionary):
    return [sorted(sublst, key=lambda x: dictionary[x]) for sublst in lst]


# def get_sorted_subgraphs(G):
#     subgraphs = list(nx.connected_components(G))
#     subgraphs = convert_lset_to_llist(subgraphs)


def repair_degree(degree_constrained, edges):
    # Tạo đồ thị cây từ danh sách cạnh
    G = nx.Graph(edges)
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


def make_graph_connected(G):
    """Biến đồ thị không liên thông trở thành liên thông"""
    # Tìm các thành phần liên thông của đồ thị
    subgraphs = list(nx.connected_components(G))
    # print(subgraphs)
    subgraphs = convert_lset_to_llist(subgraphs)

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


# def repair_pop(pop, degree_constrained):
#     for i in range(len(pop)):
#         # print("individual", i)
#         edges = decode_to_graph(compute_n(len(pop[i])), pop[i])
#         # print(edges)
#         # Làm đồ thị liên thông
#         G = make_graph_connected(nx.from_edgelist(edges))
#         print(G.edges())
#         # Xóa chu trình
#         fix_cycle(G)
#         tree = repair_degree(degree_constrained, G.edges).edges()
#         pop[i] = tree
#     return pop


# Cây có 5 đỉnh và 4 cạnh
constrained = 2
edges = [(0, 1)]
G = nx.empty_graph(5)
G = G.add_edges_from(edges)
G = make_graph_connected(G)
G = fix_cycle(G)
G = repair_degree(constrained, G.edges())
# print(G.edges)
print(G.edges)
print(encode_to_cv(10, G.edges()))
print(nx.is_tree(G))


# # Kiểm tra và sửa cây
# G = repair_degree(constrained, edges)
# pop = []
# for _ in range(5):
#     pop.append(gen_bit(5))
# print(pop)
# # repair_pop(pop, 2)
# print(pop)

# for i in range(len(pop)):
#     g = nx.Graph()
#     g.add_edges_from(pop[i])
#     print(nx.is_tree(g))
#
# e = decode_to_graph(5, [1, 1, 0, 0, 0, 0, 1, 0, 0, 1])
# print(e)
#
# tree = nx.from_edgelist(e)
# tree = make_graph_connected(tree)
# print(tree.edges)
# tree = fix_cycle(tree)
# print(tree.edges)
# print(nx.is_tree(tree))
