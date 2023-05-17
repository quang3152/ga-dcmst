import random

import networkx as nx
import numpy as np
import os
import time
# from utils_cv import *
# from utils import compute_degree
from util import *
import sys


def encode_to_cv(n, edges):
    """mã hóa đồ thị n đỉnh thành chuỗi bit"""
    g = nx.complete_graph(n)
    g_edges = list(g.edges)

    bit = [0] * len(g_edges)
    for i in range(len(g_edges)):
        if g_edges[i] in edges:
            bit[i] = 1
    return bit


def decode_to_graph(n, cv):
    g = nx.complete_graph(n)
    g_edges = list(g.edges)
    edges = []
    for i in range(len(g_edges)):
        if cv[i] == 1:
            edges.append(g_edges[i])
    return edges


def make_graph_connected(G):
    # Tìm các thành phần liên thông của đồ thị
    subgraphs = list(nx.connected_components(G))
    subgraphs = convert_lset_to_llist(subgraphs)
    # print(subgraphs)

    # Nếu đồ thị đã liên thông, không cần thực hiện gì thêm
    if len(subgraphs) == 1:
        return G

    # Thêm các cạnh để kết nối các thành phần liên thông
    for i in range(len(subgraphs) - 1):
        nodes1 = subgraphs[i]
        nodes2 = subgraphs[i + 1]
        node1 = nodes1[0]
        node2 = nodes2[0]
        G.add_edge(node1, node2)

    return G


def fix_cycle(nx_graph):
    """Đầu vào là một đồ thị liên thông"""
    while is_cycle(nx_graph):
        c = nx.find_cycle(nx_graph)
        nx_graph.remove_edge(c[1][0], c[1][1])
    return nx_graph


def is_cycle(nx_graph):
    if not nx.is_tree(nx_graph) and nx.is_connected(nx_graph):
        return True
    else:
        return False


def calculate_fitness(cv_sequence, degree_constrained, distances_table):
    n = compute_n(len(cv_sequence))
    edges = decode_to_graph(n, cv_sequence)
    T = nx.from_edgelist(edges)
    degrees = list(compute_degree(T).values())
    # print(degrees)
    isTree = nx.is_tree(T)
    if not isTree:
        return sys.maxsize
    # Check if the degrees more than target degrees
    if any(x > degree_constrained for x in degrees):
        return sys.maxsize

    cost = 0
    for edge in edges:
        cost = cost + get_distance(edge, distances_table)
    return cost


def crossover(parent1, parent2, crossover_rate=1):
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 2)
        offspring1[crossover_point:], offspring2[crossover_point:] = offspring2[crossover_point:], offspring1[
                                                                                                   crossover_point:]
    return offspring1, offspring2


def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        idx1 = individual.index(1)
        idx2 = individual.index(0)
        # idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


def mutate_pop(population, mutation_rate):
    new_pop = []
    for individual in population:
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
            new_pop.append(individual)
    return new_pop


import heapq


def get_new_pop(population, population_size, degree_constrained, distances_table):
    fitness_values = [calculate_fitness(individual, degree_constrained, distances_table) for
                      individual in population]
    sorted_fitness = sorted(fitness_values)
    index_dict = {val: idx for idx, val in enumerate(fitness_values)}
    # Lấy danh sách index của population đã được sắp xếp theo fitness
    pop_index = [index_dict[val] for val in sorted_fitness]
    # Lấy index của [population_size] phần tử đầu (có cost nhỏ nhất)
    new_pop_index = pop_index[:population_size]
    new_pop = [population[i] for i in new_pop_index]
    return new_pop


def create_new_population(population, fitness, pop_size):
    # create a list of individuals with their fitnesses
    individuals_fitness = [(population[i], fitness[i]) for i in range(len(population))]

    # create a new population with the n/2 best individuals
    best_individuals = heapq.nsmallest(pop_size // 2, individuals_fitness, key=lambda x: x[1])
    new_pop = [individual[0] for individual in best_individuals]

    # create a list of remaining individuals
    remaining_individuals = individuals_fitness[pop_size // 2:]
    # add n/2 individuals chosen randomly with the criterion of the best fitness
    for _ in range(pop_size // 2):
        # print("remaining", remaining_individuals)
        # randomly select two individuals
        ind_indices = np.random.choice(len(remaining_individuals), size=2, replace=False)
        #         print(ind_indices)
        ind1, ind2 = remaining_individuals[ind_indices[0]], remaining_individuals[ind_indices[1]]
        #         print(ind1, ind2)
        # add the individual with the highest fitness to the new population
        if ind1[1] > ind2[1]:
            new_pop.append(ind1[0])
            remaining_individuals.remove(ind1)
        else:
            new_pop.append(ind2[0])
            remaining_individuals.remove(ind2)

    return new_pop


def repair_degree(degree_constrained, G):
    # Tạo đồ thị cây từ danh sách cạnh
    # G = nx.Graph(edges)
    subgraphs = []
    # Kiểm tra giới hạn bậc của mỗi đỉnh
    for v in G.nodes():
        if G.degree(v) > degree_constrained:
            # Nếu có đỉnh có giới hạn bậc quá n, thực hiện sửa cây
            # Tìm các đỉnh kề của đỉnh này
            neighbors = list(G.neighbors(v))
            # print("v, neighbor", v, neighbors)
            # Xóa các cạnh kết nối đỉnh này với các đỉnh kề
            for i in range(len(neighbors) - degree_constrained):
                G.remove_edge(neighbors[i], v)

            subgraphs = list(nx.connected_components(G))
    subgraphs = convert_lset_to_llist(subgraphs)
    # print(subgraphs)
    degree = compute_degree(G)
    # print(degree)
    subgraphs = sort_sublists(subgraphs, degree)
    # print(subgraphs)
    while len(subgraphs) > 1:
        # Ghép 2 đồ thị đầu tiên
        G.add_edge(subgraphs[0][0], subgraphs[1][0])
        # Tính toán lại subgraph và bậc đồ thị sau khi ghép
        subgraphs = list(nx.connected_components(G))
        subgraphs = convert_lset_to_llist(subgraphs)
        degree = compute_degree(G)
        subgraphs = sort_sublists(subgraphs, degree)
        # print(subgraphs)

    # Trả về danh sách cạnh của cây đã được sửa
    return G


def repair_pop(pop, degree_constrained):
    for i in range(len(pop)):
        # print("individual", i)
        n = compute_n(len(pop[i]))
        edges = decode_to_graph(n, pop[i])
        # print("Tree: ", edges)
        G = nx.empty_graph(n)
        G.add_edges_from(edges)
        G = make_graph_connected(G)
        # print("Connect: ", G.edges)
        # print("Fix Cycle", fix_cycle(G).edges())
        repair_degree(degree_constrained, G)
        # print("Out: ", G.edges())
        # print(nx.is_tree(G))
        pop[i] = encode_to_cv(n, G.edges())
    return pop


def run_ga(n, degree_constrained, distances_table, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
           max_generations=50):
    population = [gen_bit(n) for _ in range(population_size)]
    repair_pop(population, degree_constrained)
    # print(population)
    for generation in range(max_generations):
        # print(population)
        # Tính một mảng fitness value của population
        fitness_values = [calculate_fitness(cv_sequence, degree_constrained, distances_table) for
                          cv_sequence in population]
        # print(fitness_values)
        new_population = []
        while len(new_population) < population_size:
            p = 1 / np.array(fitness_values)
            i, j = np.random.choice(range(population_size), size=2, replace=False,
                                    p=p / np.sum(p))
            parent1 = population[i]
            parent2 = population[j]
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(offspring1)
            new_population.append(offspring2)
        for i in range(len(new_population)):
            mutate(new_population[i])
        repair_pop(new_population, degree_constrained)
        new_fitness = [calculate_fitness(prufer_sequence, degree_constrained, distances_table) for
                       prufer_sequence in new_population]
        fitness = fitness_values + new_fitness

        population = population + new_population
        population = create_new_population(population, fitness, population_size)

    return population


def write_result(results, filename):
    path_result = "result"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['STT', 'Best Cost', 'Best Solution', 'Best Tree', 'Time', 'Is Tree?'])

        # Ghi từng dòng kết quả
        for result in results:
            writer.writerow(result)


degree_constrained = 3
n = 8
path = "data/8_nodes"
# list_file = os.listdir(path)
list_file = [file_name for file_name in os.listdir(path) if file_name.endswith(".csv")]
folder = path.replace("data", "result/result_cv")
if not os.path.exists(folder):
    os.mkdir(folder)
print(list_file)
for file in list_file:
    print(file)
    results = []
    path_to_data = os.path.join(path, file)
    dis_tab = get_distance_table(path_to_data)
    path_to_result = path_to_data.replace("data", "result/result_cv")
    path_to_result = path_to_result.replace("\\", "/")
    # print(path_to_result)
    for i in range(10):
        print("Loop: ", i + 1, "...")
        start_time = time.time()
        population = run_ga(n, degree_constrained, dis_tab)
        best_solution = population[0]
        best_cost = calculate_fitness(best_solution, n, dis_tab)
        best_tree = decode_to_graph(n, best_solution)
        end_time = time.time()
        G = nx.from_edgelist(best_tree)
        isTree = nx.is_tree(G)
        elapsed_time = end_time - start_time
        row = (i + 1, best_cost, best_solution, best_tree, elapsed_time, isTree)
        results.append(row)
    print("Result 10 times", results)

    # print(path_to_result)
    write_result(results, path_to_result)
