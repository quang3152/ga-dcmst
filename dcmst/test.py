import networkx as nx
from utils import *


def find(parents, i):
    if parents[i] == i:
        return i
    parents[i] = find(parents, parents[i])
    return parents[i]


def union(parents, ranks, i, j):
    root_i = find(parents, i)
    root_j = find(parents, j)
    if root_i == root_j:
        return
    if ranks[root_i] < ranks[root_j]:
        parents[root_i] = root_j
    elif ranks[root_i] > ranks[root_j]:
        parents[root_j] = root_i
    else:
        parents[root_j] = root_i
        ranks[root_i] += 1


def make_tree(edges):
    n = len(edges) + 1
    parents = [i for i in range(n)]
    ranks = [0] * n
    tree = []
    for u, v in edges:
        if find(parents, u) != find(parents, v):
            tree.append((u, v))
            union(parents, ranks, u, v)
    return tree


# G = nx.complete_graph(5)
edges = [(0, 1), (1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (6, 7), (3, 4)]
G = nx.from_edgelist(edges)
print(nx.is_connected(G))
print([len(c) for c in sorted(nx.connected_components(G))])
tree = make_tree(edges)
print(tree)
