import random

import networkx as nx
import numpy as np
from utils_cv import compute_n, is_cycle
from utils import *


# def construct_tree_from_rks(r: str, n: int) -> nx.Graph:
#     # Construct permutation from RK sequence
#     l = n * (n - 1) // 2
#     rs = [int(r[i:i + 8], 16) % l for i in range(0, 16 * n, 16)]
#
#     # Construct tree from permutation
#     T = nx.Graph()
#     T.add_nodes_from(range(n))
#     i = 0
#     while len(T.edges) < n - 1:
#         j = rs[i]
#         i += 1
#         # Check if adding edge j would create a cycle
#         if not nx.has_path(T, *T.edges[j]):
#             T.add_edge(*T.nodes[j])
#     return T


def get_permutation(random_key_sequence):
    key = np.array(random_key_sequence)
    return np.argsort(key)[::-1]


def decode(permutation, degree_constrained):
    n = compute_n(len(permutation))
    G = nx.complete_graph(n)
    # print("Full G:", G.edges)
    # print(G.edges[4])
    edges = list(G.edges)

    T = nx.empty_graph(n)
    # print(T.nodes)
    i = 0
    while len(T.edges) < n - 1:
        # T.add_edge(G.edges[i])
        j = permutation[i]
        # print(j)
        i += 1
        edge = edges[j]
        # print(edge)
        T.add_edge(*edge)
        nodes = [*edge]
        # print("Edge:", edge)
        # print("T:", T.edges)
        # print("Circle:", is_cycle(T))
        # print("Constrain:", T.degree(nodes[0]) > degree_constrained, T.degree(nodes[1]) > degree_constrained)
        if is_cycle(T):
            T.remove_edge(*edge)
        elif T.degree(nodes[0]) > degree_constrained or T.degree(nodes[1]) > degree_constrained:
            T.remove_edge(*edge)

    return T


def gen_key(n):
    l = int(n * (n - 1) / 2)
    return [random.random() for _ in range(l)]


# lst = [0.39030213827774307, 0.6308759158260975, 0.1397273653286547, 0.420702941912681, 0.45982562220982404,
#        0.2851033174470138, 0.1823421862752288, 0.6555169505758537, 0.7082570255982881, 0.7659866011992312]
lst = gen_key(7)
print(lst)
permutation = get_permutation(lst)
print("Permutation:", permutation)
tree = decode(permutation, 2)
print("Tree:", tree.edges)
print(nx.is_tree(tree))


def compute_degrees(edges):
    degrees = {}
    for edge in edges:
        for vertex in edge:
            if vertex not in degrees:
                degrees[vertex] = 0
            degrees[vertex] += 1
    return degrees


def calculate_fitness(random_key_sequence, degree_constrained, distances_table):
    permutation = get_permutation(random_key_sequence)
    tree = decode(permutation, degree_constrained)
    edges = tree.edges
    # # Check if the degrees more than target degrees
    # if any(x > degree_constrained for x in degrees):
    #     return 9999999

    cost = 0
    for edge in edges:
        cost = cost + get_distance(edge, distances_table)
    return cost


distance_table = get_distance_table("")
key = gen_key(10)
print(key)
print(calculate_fitness(key, 2, distance_table))

