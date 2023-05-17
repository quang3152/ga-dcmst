import csv
import math
import random
import networkx as nx


# # For general

# Get a dictionary containing the distances between vertices from the dataset
def get_distance_table(file_path):
    records = []
    # Read .csv data
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            records.append(row)

    # Create a dictionary to store distances between vertices
    distances_table = {}

    # Calculate distance between vertices and store result into dictionary
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            point1 = (float(records[i][1]), float(records[i][2]))
            point2 = (float(records[j][1]), float(records[j][2]))
            distance = math.dist(point1, point2)
            key = (int(records[i][0]), int(records[j][0]))
            distances_table[key] = distance

    # Returns the distance dictionary
    return distances_table


# Get the distance of 1 edge/between 2 vertices
def get_distance(edge, distances_table):
    if edge in distances_table:
        return distances_table[edge]
    if edge[::-1] in distances_table:
        return distances_table[edge[::-1]]


# Convert a list of sets to a list of lists
def convert_lset_to_llist(lset):
    llist = [list(item) for item in lset]
    return llist


# Calculate the degree of each vertex in the graph
def compute_degree(G):
    degree = {}
    nodes = G.nodes
    for i in nodes:
        degree[i] = G.degree(i)
    return degree


def sort_sublists(lst, dictionary):
    return [sorted(sublst, key=lambda x: dictionary[x]) for sublst in lst]


# Sort dictionary by value
def sort_by_value(dictionary):
    return dict(sorted(dictionary.items(), key=lambda x: x[1]))


# # For CV

# Calculate the number of vertices from the input key sequence
def compute_n(len):
    delta = 1 + 8 * len
    sqrt_delta = math.sqrt(delta)
    n = int((1 + sqrt_delta) / 2)
    return n


# Generate characteristic vector with n-1 elements 1
def gen_bit(n):
    # Calculate the number of elements in the characteristic vector
    m = n * (n - 1) // 2
    # Initialize vector all elements are 0
    bit = [0] * m
    # Randomly select n-1 positions and set their value to 1
    ones = random.sample(range(m), n - 1)
    for idx in ones:
        bit[idx] = 1
    return bit


# Encode the graph of n vertices into a characteristic vector
def encode_to_cv(n, edges):
    g = nx.complete_graph(n)
    g_edges = list(g.edges)

    bit = [0] * len(g_edges)
    for i in range(len(g_edges)):
        if g_edges[i] in edges:
            bit[i] = 1
    return bit


# Decode the characteristic vector into a graph
def decode_to_graph(n, cv):
    g = nx.complete_graph(n)
    g_edges = list(g.edges)
    edges = []
    for i in range(len(g_edges)):
        if cv[i] == 1:
            edges.append(g_edges[i])
    return edges


# Make an unconnected graph connected
def make_graph_connected(G):
    # Find the connected components of a graph
    subgraphs = list(nx.connected_components(G))

    # If the graph is connected, no further action is needed
    if len(subgraphs) == 1:
        return G

    # Adding edges to connect connected components
    for i in range(len(subgraphs) - 1):
        nodes1 = subgraphs[i]
        nodes2 = subgraphs[i + 1]
        node1 = nodes1.pop()
        node2 = nodes2.pop()
        G.add_edge(node1, node2)
    return G


# Check if graph has a cycle or not
def is_cycle(G):
    try:
        if nx.find_cycle(G):
            return True
        else:
            return False
    except:
        return False


# Remove cycles (Input must be a connected graph)
def fix_cycle(nx_graph):
    while is_cycle(nx_graph):
        c = nx.find_cycle(nx_graph)
        nx_graph.remove_edge(c[1][0], c[1][1])
    return nx_graph


# Write the results to a .csv file
def write_result(results, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['STT', 'Best Cost', 'Best Solution', 'Best Tree', 'Time'])
        for result in results:
            writer.writerow(result)

