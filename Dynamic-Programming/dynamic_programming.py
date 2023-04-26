import numpy as np

# Function to calculate the shortest path between cities for a given salesman
def tsp(distances, n, m, salesman, current_city, visited_cities, memo):
    # Base case: if all cities have been visited, return the distance to the starting city
    if len(visited_cities) == n:
        return distances[current_city, 0]
    
    # If the current state has already been computed, return the memoized value
    if (current_city, tuple(visited_cities)) in memo:
        return memo[(current_city, tuple(visited_cities))]
    
    # Otherwise, compute the shortest path recursively
    shortest_path = np.inf
    for city in range(1, n):
        if city not in visited_cities:
            new_visited_cities = visited_cities.union(set([city]))
            cost = distances[current_city, city] + tsp(distances, n, m, salesman, city, new_visited_cities, memo)
            shortest_path = min(shortest_path, cost)
    
    # Memoize the result and return it
    memo[(current_city, tuple(visited_cities))] = shortest_path
    return shortest_path

# Function to solve the MTSP using dynamic programming
def solve_mtsp(distances, n, m):
    # Initialize the memoization dictionary
    memo = {}
    
    # Initialize the optimal path and its length
    optimal_path = [set([0]) for _ in range(m)]
    optimal_length = np.inf
    
    # Try all possible combinations of cities visited by each salesman
    for mask in range(1, (1 << n)):
        # Count the number of cities visited by each salesman
        num_visited_cities = [bin(mask).count("1") for _ in range(m)]
    
        # Check that every salesman has visited at least one city
        if all(num_visited_cities[j] > 0 for j in range(m)):
    
            # Initialize the visited cities and the path lengths for each salesman
            visited_cities = [set([0]) for _ in range(m)]
            path_lengths = [0] * m
    
            # Update the visited cities and the path lengths based on the mask
            for city in range(n):
                salesman = city % m
                if (mask >> city) & 1:
                    visited_cities[salesman].add(city)
                    path_lengths[salesman] += distances[(city - 1) % n, city]
    
            # Calculate the shortest path for each salesman
            shortest_paths = []
            for salesman in range(m):
                shortest_path = tsp(distances, n, m, salesman, 0, visited_cities[salesman], memo)
                shortest_paths.append(shortest_path)
    
            # If this combination is better than the current optimal, update the optimal path and length
            if sum(shortest_paths) < optimal_length:
                for salesman in range(m):
                    optimal_path[salesman] = visited_cities[salesman].copy()
                optimal_length = sum(shortest_paths)

    
    return optimal_path, optimal_length

# Take input from the user
m = int(input("Enter the number of salesmen: "))
n = int(input("Enter the number of cities: "))

# Generate random coordinates for cities
cities = np.random.randint(1, n, size=(n, 2))
print(cities)

# Calculate the distances between cities
distances = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        distances[i, j] = np.sqrt((cities[i, 0] - cities[j, 0])**2 + (cities[i, 1] - cities[j, 1])**2)
        print("{:.2f}".format(distances[i, j]), end=" ")
    print()

# Solve the MTSP using dynamic programming
optimal_path, optimal_length = solve_mtsp(distances, n, m)

# Print the optimal path and length
print("Optimal path:", optimal_path)
print("Optimal length:", optimal_length)
