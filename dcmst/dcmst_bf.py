import ast
import csv
import os
import sys
import time

import networkx as nx

from util import get_distance, get_distance_table, write_result


def read_txt_file(file_path):
    # Khởi tạo danh sách rỗng
    tree = []

    try:
        # Mở tệp văn bản để đọc
        with open(file_path, 'r') as file:
            # Đọc từng dòng trong tệp và thêm nó vào danh sách
            for line in file:
                tree.append(line.strip())  # strip() để loại bỏ ký tự xuống dòng (\n)

    except IOError:
        print("Không thể đọc tệp:", file_path)

    # Trả về danh sách tree
    return tree


def calculate_fitness(list_edges, degree_constrained, distances_table):
    # print(len(list_edges))
    list_edges = ast.literal_eval(list_edges)

    G = nx.Graph()
    G.add_edges_from(list_edges)
    degrees = list(map(lambda x: x[1], G.degree()))
    # print(degrees)

    # Check if the degrees more than target degrees
    if any(x > degree_constrained for x in degrees):
        return sys.maxsize

    cost = 0
    for edge in list_edges:
        cost = cost + get_distance(edge, distances_table)
    return cost


def run_bf(data_path, tree_path, degree_constrained):
    # Gọi hàm để đọc tệp và lưu nội dung vào danh sách
    spanning_trees = read_txt_file(tree_path)
    dis_tab = get_distance_table(data_path)
    # i = 1
    min_cost = sys.maxsize
    best_tree = []
    for tree in spanning_trees:
        # print(tree)
        cost = calculate_fitness(tree, degree_constrained=degree_constrained, distances_table=dis_tab)
        # print(cost, tree)
        if cost < min_cost:
            best_tree = tree
            min_cost = cost
        # print("best_tree", min_cost, best_tree)
    print("Tree:", best_tree)
    print("Cost: ", min_cost)
    return best_tree, min_cost


def write_result(results, filename):
    path_result = "result"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['STT', 'Best Tree', 'Best Cost'])

        # Ghi từng dòng kết quả
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    path = "data/8_nodes"
    tree_path = "data/8_nodes.txt"
    degree_constrained = 3
    list_file = os.listdir(path)
    print(list_file)
    file = open("result/result_bf/bf.csv", 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['Instance', 'Best Tree', 'Best Cost'])
    for file in list_file:
        print(file)
        results = []
        path_to_data = os.path.join(path, file)
        # dis_tab = get_distance_table(path_to_data)
        path_to_result = path_to_data.replace("data", "result/result_bf")
        path_to_result = path_to_result.replace("\\", "/")
        # print(path_to_result.split("/"))
        folder = path_to_result.split("/")[0] + "/" + path_to_result.split("/")[1]
        if not os.path.exists(folder):
            os.mkdir(folder)
        # print(path_to_result)
        best_tree, min_cost = run_bf(path_to_data, tree_path, degree_constrained)
        row = (path_to_result.split("/")[-1], best_tree, min_cost)
        writer.writerow(row)
