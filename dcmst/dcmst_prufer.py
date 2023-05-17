import heapq
import os
import random
import time

import networkx as nx
import numpy as np
import math
import csv
from sys import maxsize


def gen_prufer(degree_constrained, n):
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


# Đọc dữ liệu từ tệp CSV và lưu trữ nó trong danh sách
def get_distance_table(file_path):
    records = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
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


def get_distance(edge, distances_table):
    if edge in distances_table:
        return distances_table[edge]
    if edge[::-1] in distances_table:
        return distances_table[edge[::-1]]


def compute_degrees(edges):
    degrees = {}
    for edge in edges:
        for vertex in edge:
            if vertex not in degrees:
                degrees[vertex] = 0
            degrees[vertex] += 1
    return degrees


def calculate_fitness(prufer_sequence, degree_constrained, distances_table):
    tree = nx.from_prufer_sequence(prufer_sequence)
    edges = tree.edges
    degrees = list(compute_degrees(edges).values())
    # print(degrees)

    # Check if the degrees more than target degrees
    if any(x > degree_constrained for x in degrees):
        return 9999999

    cost = 0
    for edge in edges:
        cost = cost + get_distance(edge, distances_table)
    return cost


def crossover(parent1, parent2, crossover_rate=1):
    offspring1 = parent1[:]
    offspring2 = parent2[:]
    # print(parent1, parent2)
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 2)
        # print("c point: ", crossover_point)
        offspring1[crossover_point:], offspring2[crossover_point:] = offspring2[crossover_point:], offspring1[
                                                                                                   crossover_point:]
    return offspring1, offspring2


def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
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


def sort_by_value(dict):
    return sorted(dict.items(), key=lambda x: x[1])


def repair(prufer_sequence, degree_constrained):
    set_ver = set(range(len(prufer_sequence) + 2))
    count = {}
    for ver in set_ver:
        count[ver] = prufer_sequence.count(ver)
    count = dict(sort_by_value(count))

    for i in range(len(prufer_sequence)):
        if count[prufer_sequence[i]] > degree_constrained - 1:
            j = next(iter(count))
            count.update([(prufer_sequence[i], count[prufer_sequence[i]] - 1), (j, count[j] + 1)])
            prufer_sequence[i] = j
            count = dict(sort_by_value(count))
    return prufer_sequence


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


def run_ga(n, degree_constrained, distances_table, population_size=50, crossover_rate=0.8, mutation_rate=0.1,
           max_generations=50):
    population = [gen_prufer(degree_constrained, n) for _ in range(population_size)]

    for generation in range(max_generations):
        # Tính một mảng fitness value của population
        fitness_values = [calculate_fitness(prufer_sequence, degree_constrained, distances_table) for
                          prufer_sequence in population]
        # print(population)
        # print(fitness_values)
        new_population = []
        while len(new_population) < population_size:
            i, j = np.random.choice(range(population_size), size=2, replace=False,
                                    p=np.array(fitness_values) / sum(fitness_values))
            parent1 = population[i]
            parent2 = population[j]
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(offspring1)
            new_population.append(offspring2)
        for i in range(len(new_population)):
            mutate(new_population[i])
            #             print(new_population[i])
            repair(new_population[i], degree_constrained)
        #             print(new_population[i])

        #         print(new_population)
        new_fitness = [calculate_fitness(prufer_sequence, degree_constrained, distances_table) for
                       prufer_sequence in new_population]
        #         print(new_fitness)
        fitness = fitness_values + new_fitness

        #         print(fitness)
        population = population + new_population
        population = create_new_population(population, fitness, population_size)
        # population = get_new_pop(population, population_size, degree_constrained, distances_table)

    return population


def write_result(results, filename):
    path_result = "result"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['STT', 'Best Cost', 'Best Solution', 'Best Tree', 'Time'])

        # Ghi từng dòng kết quả
        for result in results:
            writer.writerow(result)


def main(path, degree_constrained, n):
    # path = "data/15"
    list_file = os.listdir(path)
    folder = path.replace("data", "result/result_pr")
    if not os.path.exists(folder):
        os.mkdir(folder)
    print(list_file)
    for file in list_file:
        print(file)
        results = []
        path_to_data = os.path.join(path, file)
        dis_tab = get_distance_table(path_to_data)
        path_to_result = path_to_data.replace("data", "result/result_pr")
        path_to_result = path_to_result.replace("\\", "/")
        # print(path_to_result)
        for i in range(10):
            print("Loop: ", i + 1, "...")
            start_time = time.time()
            population = run_ga(n, degree_constrained, dis_tab)
            best_solution = population[0]
            best_cost = calculate_fitness(best_solution, n, dis_tab)
            best_tree = nx.from_prufer_sequence(population[0]).edges()
            end_time = time.time()
            elapsed_time = end_time - start_time
            row = (i + 1, best_solution, best_cost, best_tree, elapsed_time)
            results.append(row)
        print("Result 10 times", results)

        # print(path_to_result)
        write_result(results, path_to_result)


if __name__ == '__main__':
    data_path = "data/8_nodes"
    degree_constrained = 3
    number_of_nodes = 8
    main(data_path, degree_constrained, number_of_nodes)
