import random
import sys
import networkx as nx
import numpy as np
# from utils_cv import compute_n, is_cycle
# from utils import get_distance_table, get_distance, write_result
from utils import compute_n, is_cycle, get_distance_table, get_distance
import heapq
import os
import time
import csv


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


def calculate_fitness(random_key_sequence, degree_constrained, distances_table):
    permutation = get_permutation(random_key_sequence)
    tree = decode(permutation, degree_constrained)
    edges = tree.edges
    # # Check if the degrees more than target degrees
    # if any(x > degree_constrained for x in degrees):
    #     return sys.maxsize

    cost = 0
    for edge in edges:
        cost = cost + get_distance(edge, distances_table)
    return cost


def crossover(parent1, parent2, crossover_rate=0.8):
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 2)
        offspring1[crossover_point:], offspring2[crossover_point:] = offspring2[crossover_point:], offspring1[
                                                                                                   crossover_point:]
    return offspring1, offspring2


def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


# def mutate_pop(population, mutation_rate):
#     new_pop = []
#     for individual in population:
#         if random.random() < mutation_rate:
#             idx1, idx2 = random.sample(range(len(individual)), 2)
#             individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
#             new_pop.append(individual)
#     return new_pop


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


def run_ga(n, degree_constrained, distances_table, population_size=80, crossover_rate=0.8, mutation_rate=0.1,
           max_generations=50):
    population = [gen_key(n) for _ in range(population_size)]
    # print(population)
    for generation in range(max_generations):
        # print(population)
        # Tính một mảng fitness value của population
        fitness_values = [calculate_fitness(cv_sequence, degree_constrained, distances_table) for
                          cv_sequence in population]
        # print(fitness_values)
        new_population = []
        while len(new_population) < population_size:
            i, j = np.random.choice(range(population_size), size=2, replace=False,
                                    p=np.array(fitness_values) / sum(fitness_values))
            parent1 = population[i]
            parent2 = population[j]
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)
            new_population.append(offspring1)
            new_population.append(offspring2)
        for i in range(len(new_population)):
            mutate(new_population[i], mutation_rate)
        new_fitness = [calculate_fitness(prufer_sequence, degree_constrained, distances_table) for
                       prufer_sequence in new_population]
        fitness = fitness_values + new_fitness

        population = population + new_population
        population = create_new_population(population, fitness, population_size)
        # population = get_new_pop(population, population_size, degree_constrained, distances_table)

    return population


def write_result(results, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['STT', 'Best Cost', 'Best Tree', 'Time', 'Is Tree?'])

        # Ghi từng dòng kết quả
        for result in results:
            writer.writerow(result)


def main(path, degree_constrained, n):
    # path = "data/15"
    list_file = os.listdir(path)
    folder = path.replace("data", "result/result_nk")
    if not os.path.exists(folder):
        os.makedirs(folder)
    print(list_file)
    for file in list_file:
        print(file)
        results = []
        path_to_data = os.path.join(path, file)
        dis_tab = get_distance_table(path_to_data)
        path_to_result = path_to_data.replace("data", "result/result_nk")
        path_to_result = path_to_result.replace("\\", "/")
        # print(path_to_result)
        for i in range(10):
            print("Loop: ", i + 1, "...")
            start_time = time.time()

            population = run_ga(n, degree_constrained, dis_tab)

            best_solution = population[0]
            best_cost = calculate_fitness(best_solution, n, dis_tab)
            permutation = get_permutation(population[0])
            best_tree = decode(permutation, degree_constrained).edges()
            end_time = time.time()
            G = nx.from_edgelist(best_tree)
            isTree = nx.is_tree(G)
            elapsed_time = end_time - start_time
            row = (i + 1, best_cost, best_tree, elapsed_time, isTree)
            results.append(row)
        print("Result 10 times", results)

        # print(path_to_result)
        write_result(results, path_to_result)


if __name__ == '__main__':
    data_path = "data/8_nodes"
    degree_constrained = 3
    number_of_nodes = 8
    main(data_path, degree_constrained, number_of_nodes)
