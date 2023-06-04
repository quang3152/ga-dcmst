import numpy as np

# Ví dụ mảng fitness_values ban đầu
fitness_values = np.array([10, 20, 30, 40, 50])

# Đảo ngược các giá trị trong fitness_values (giá trị bé nhất sẽ trở thành lớn nhất và ngược lại)
reversed_fitness_values = 1 / fitness_values
print(reversed_fitness_values)
# Tính tổng các giá trị đã đảo ngược
sum_reversed_fitness = np.sum(reversed_fitness_values)

# Tính mảng xác suất
probabilities = reversed_fitness_values / sum_reversed_fitness

print(probabilities)  # in ra mảng xác suất
