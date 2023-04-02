import networkx as nx

from utils import *


# def encode_to_cv(n, edges):
#     """mã hóa đồ thị n đỉnh thành chuỗi bit"""
#     g = nx.complete_graph(n)
#     g_edges = list(g.edges)
#
#     cv = [0] * len(g_edges)
#     for i in range(len(g_edges)):
#         if g_edges[i] in edges:
#             cv[i] = 1
#     return cv
#
#
# def decode_to_graph(n, cv):
#     g = nx.complete_graph(n)
#     g_edges = list(g.edges)
#     edges = []
#     for i in range(len(g_edges)):
#         if cv[i] == 1:
#             edges.append(g_edges[i])
#     return edges
#
#
# n = 4
# edges = [(0, 1), (1, 2), (2, 3), (1, 3)]
# cv = [1, 1, 0, 0, 0, 1]
# print(encode_to_cv(n, edges))
# print(decode_to_graph(n, cv))
#
# g = nx.from_edgelist(edges)
# print(g.edges(2))


def repair(nx_graph, degree_constrained):
    # Sắp xếp theo giá trị bậc (sắp xếp dict theo value)
    # ví dụ {0: 1, 1: 3, 2: 2, 3: 2}
    # sắp xếp thành: {0: 1, 2: 2, 3: 2, 1: 3}
    degree = compute_degrees(nx_graph.edges)
    print(degree)
    sorted_degree = sort_by_value(degree)
    print(sorted_degree)
    # Cặp k-v cuối luôn có bậc cao nhất -> check nó với giới hạn bậc
    # Nếu lớn hơn
    while next(reversed(sorted_degree.values())) > degree_constrained:
        # Lấy các cạch nối với đỉnh bậc cao nhất
        edges = nx_graph.edges(next(reversed(sorted_degree.keys())))
        print(edges)
        # Loại bỏ 1 cạnh nối với đỉnh
        rm_edge = list(edges)[0]
        nx_graph.remove_edge(rm_edge[0], rm_edge[1])

        add_edge = rm_edge[1], next(iter(sorted_degree.keys()))
        # Thêm cạnh của đỉnh nối với đỉnh có bậc cao nhất (vừa bị xóa) với đỉnh có bậc nhỏ nhất
        if not nx_graph.has_edge(add_edge[0], add_edge[1]):
            nx_graph.add_edge(add_edge[0], add_edge[1])
            sorted_degree.update(
                [(rm_edge[0], sorted_degree[rm_edge[0]] - 1), (add_edge[1], sorted_degree[add_edge[1]] + 1)])

        sorted_degree.update([(rm_edge[0], sorted_degree[rm_edge[0]] - 1), (add_edge[1], sorted_degree[add_edge[1]] + 1)])
        sorted_degree = sort_by_value(sorted_degree)

    print(nx.is_tree(nx_graph))
    return nx_graph


edges = [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5)]
G = nx.from_edgelist(edges)
repair(G, 2)
print(G.edges)
