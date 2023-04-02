import networkx as nx

def limit_degree_tree(G, n):
    T = nx.Graph()
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    for u, v, d in edges:
        if T.degree(u) < n and T.degree(v) < n:
            T.add_edge(u, v, weight=d['weight'])
            if nx.is_tree(T):
                return T
            # if the graph is disconnected
            if nx.number_connected_components(T) > 1:
                return None
    return None
import random

G = nx.Graph()

for i in range(10):
    G.add_node(i)

for i in range(20):
    u, v = random.sample(range(10), 2)
    w = random.randint(1, 10)
    G.add_edge(u, v, weight=w)
from test_3 import make_graph_connected
G = make_graph_connected(G)
T = limit_degree_tree(G, 3)
import matplotlib.pyplot as plt

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.title('Graph G')
plt.axis('off')
plt.show()

nx.draw_networkx_nodes(T, pos)
nx.draw_networkx_edges(T, pos)
nx.draw_networkx_labels(T, pos)
plt.title('Tree T with max degree limit 3')
plt.axis('off')
plt.show()
