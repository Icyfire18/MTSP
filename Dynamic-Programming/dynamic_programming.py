import numpy as np
import matplotlib.pyplot as plt


# Calculate shortest path for a given salesman
def tsp(distance_matrix, n, m, salesman, current_city, visited_cities, memoized):
    # If all cities are visited
    if len(visited_cities) == n:
        return distance_matrix[current_city, 0]

    # Return the memoized value if it exists
    if (current_city, tuple(visited_cities)) in memoized:
        return memoized[(current_city, tuple(visited_cities))]

    # Initialize shortest path to infinity 
    shortest_path = np.inf
    # Compute the shortest path recursively
    for city in range(1, n):
        if city not in visited_cities:
            new_visited_cities = visited_cities.union(set([city]))
            cost = distance_matrix[current_city, city] + tsp(distance_matrix, n, m, salesman, city, new_visited_cities, memoized)
            shortest_path = min(shortest_path, cost)

    # Memoize the result and return it
    memoized[(current_city, tuple(visited_cities))] = shortest_path
    return shortest_path


# Solve MTSP using dynamic programming
def mtsp(distance_matrix, n, m):
    # Initialize the memoization dictionary
    memoized = {}

    # Initialize the optimal path to none and its length to infinity
    # Global values
    optimal_path = [set([0]) for _ in range(m)]
    optimal_length = np.inf

    # Check all possible combinations of cities visited by each salesman
    for mask in range(1, (1 << n)):
        # Number of cities visited by each salesman
        num_visited_cities = [bin(mask).count("1") for _ in range(m)]

        # Check if all salesman have visited at least one city
        if all(num_visited_cities[j] > 0 for j in range(m)):

            # Initialize the visited cities and the path lengths for each salesman
            # Local values
            visited_cities = [set([0]) for _ in range(m)]
            path_lengths = [0] * m

            # Update visited cities and path lengths on the basis of mask
            for city in range(n):
                salesman = city % m
                if (mask >> city) & 1:
                    visited_cities[salesman].add(city)
                    path_lengths[salesman] += distance_matrix[(city - 1) % n, city]

            # Shortest path for each salesman
            shortest_paths = []
            for salesman in range(m):
                shortest_path = tsp(distance_matrix, n, m, salesman, 0, visited_cities[salesman], memoized)
                shortest_paths.append(shortest_path)

            # If current combination is better than the current optimal
            # update the optimal path and length
            if sum(shortest_paths) < optimal_length:
                for salesman in range(m):
                    optimal_path[salesman] = visited_cities[salesman].copy()
                optimal_length = sum(shortest_paths)

    return optimal_path, optimal_length


# Take input from the user
m = int(input("Enter the number of salesmen: "))
n = int(input("Enter the number of cities: "))

# Track Tiem Taken
import time
start_time = time.time()

# Generate random coordinates for cities
cities = np.random.randint(1, n, size=(n, 2))
print(cities)

# Calculate the distance matrix
distance_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        distance_matrix[i, j] = np.sqrt((cities[i, 0] - cities[j, 0]) ** 2 + (cities[i, 1] - cities[j, 1]) ** 2)
        print("{:.2f}".format(distance_matrix[i, j]), end=" ")
    print()

optimal_path, optimal_length = mtsp(distance_matrix, n, m)

## Outputs
print("Process finished --- %s seconds ---" % (time.time() - start_time))
print("Optimal path:", optimal_path)
print("Optimal length:", optimal_length)
