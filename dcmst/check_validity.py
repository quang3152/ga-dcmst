import ast

import networkx as nx
import pandas as pd

# đọc file csv và lưu dữ liệu vào một DataFrame
df = pd.read_csv('result_nk/60_nodes/d60_14.csv')

# truy cập cột "Best Tree" và lưu vào một Series
best_tree_col = df['Best Tree']


def check_deg(list_degrees, degree_constrained):
    for tup in list_degrees:
        if tup[1] > degree_constrained:
            return False
    return True


# in ra các giá trị của cột "Best Tree"
for val in best_tree_col:
    list_output = ast.literal_eval(val)
    G = nx.from_edgelist(list_output)
    # print(nx.is_tree(G))
    print(check_deg(G.degree(), 3))
