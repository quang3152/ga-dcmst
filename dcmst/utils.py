# Đọc dữ liệu từ tệp CSV và lưu trữ nó trong danh sách
import csv
import math
import random


def get_distance_table(file_path):
    records = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # next(reader) # Skip header row
        for row in reader:
            records.append(row)

    # Tạo từ điển để lưu trữ khoảng cách giữa các điểm
    distances_table = {}

    # Tính toán khoảng cách giữa các điểm và lưu trữ kết quả vào từ điển
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            point1 = (float(records[i][1]), float(records[i][2]))
            point2 = (float(records[j][1]), float(records[j][2]))
            distance = math.dist(point1, point2)
            key = (int(records[i][0]), int(records[j][0]))
            distances_table[key] = distance

    # In ra từ điển khoảng cách
    return distances_table

print(get_distance_table("data/7_wi29.csv"))

def get_distance(edge, distances_table):
    if edge in distances_table:
        return distances_table[edge]
    if edge[::-1] in distances_table:
        return distances_table[edge[::-1]]


# def compute_degrees(edges):
#     degrees = {}
#     for edge in edges:
#         for vertex in edge:
#             if vertex not in degrees:
#                 degrees[vertex] = 0
#             degrees[vertex] += 1
#     return degrees
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


def sort_by_value(dictionary):
    return dict(sorted(dictionary.items(), key=lambda x: x[1]))


def compute_n(len):
    delta = 1 + 8 * len
    sqrt_delta = math.sqrt(delta)
    n = int((1 + sqrt_delta) / 2)
    return n


def gen_bit(n):
    # Tính số lượng phần tử trong danh sách
    m = n * (n - 1) // 2
    # Khởi tạo danh sách toàn bộ phần tử đều bằng 0
    bit = [0] * m
    # Chọn ngẫu nhiên n-1 vị trí và đặt giá trị của chúng thành 1
    ones = random.sample(range(m), n - 1)
    for idx in ones:
        bit[idx] = 1

    return bit


print(compute_n(45))
