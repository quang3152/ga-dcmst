import random

import networkx


def gen_prufer(n, degree_constrained):
    # Tạo danh sách ban đầu
    initial_list = list(range(n))
    # Trộn ngẫu nhiên danh sách ban đầu
    random.shuffle(initial_list)
    # Tạo danh sách mới bằng cách lấy (degree_constrained-1) phần tử đầu tiên
    prufer_sequence = initial_list[:degree_constrained - 1]
    # Nếu danh sách mới chưa đủ n-2 phần tử thì lặp lại
    while len(prufer_sequence) < n - 2:
        # Trộn ngẫu nhiên lại danh sách ban đầu
        random.shuffle(initial_list)
        # Lấy phần tử đầu tiên của danh sách ban đầu nếu không nằm trong danh sách mới quá degree_constrained
        for item in initial_list:
            if prufer_sequence.count(item) < degree_constrained:
                prufer_sequence.append(item)
                break
    # Trả về danh sách mới
    return prufer_sequence


def sort_by_value(dict):
    return sorted(dict.items(), key=lambda x: x[1])


def repair(prufer_sequence, degree_constrained):
    set_ver = set(range(len(prufer_sequence) + 2))
    count = {}
    for ver in set_ver:
        count[ver] = prufer_sequence.count(ver)
    count = dict(sort_by_value(count))

    for i in range(len(prufer_sequence)):
        if count[prufer_sequence[i]] > degree_constrained-1:
            j = next(iter(count))
            count.update([(prufer_sequence[i], count[prufer_sequence[i]] - 1), (j, count[j] + 1)])
            prufer_sequence[i] = j
            count = dict(sort_by_value(count))
    return prufer_sequence


p = [4, 4, 2, 4]
print(repair(p, 3))

import networkx as nx
G = nx.Graph()
G.add_edges_from([(0, 3), (0, 12), (0, 14), (1, 4), (2, 8), (2, 14), (3, 13), (4, 12), (5, 6), (5, 10), (6, 7), (8, 10), (9, 11), (11, 13)])

print(nx.is_tree(G))
print(G.degree)