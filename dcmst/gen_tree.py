import sys
from itertools import combinations

import networkx as nx


# from utils import get_distance, get_distance_table


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1


def generate_spanning_trees(n):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for i in range(2 ** (n * (n - 1) // 2)):
        tree_edges = []
        idx = i
        for u, v in edges:
            if idx % 2 == 1:
                tree_edges.append((u, v))
            idx //= 2
        if is_spanning_tree(n, tree_edges):
            yield tree_edges


def is_spanning_tree(n, edges):
    if len(edges) != n - 1:
        return False
    uf = UnionFind(n)
    for u, v in edges:
        if uf.find(u) == uf.find(v):
            return False
        uf.union(u, v)
    return True


if __name__ == "__main__":
    n = 5
    filename = str(n) + "_nodes.txt"
    path = "data/" + filename
    treelist = list(generate_spanning_trees(n))
    with open(path, "w") as file:
        for item in treelist:
            # print(str(item))
            file.write(str(item) + "\n")
