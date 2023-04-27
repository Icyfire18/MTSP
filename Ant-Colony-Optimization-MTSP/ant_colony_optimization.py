import numpy as np
import matplotlib.pyplot as plt
import random

# Number of cities (input from user)
n = int(input("Enter the number of cities per salesman:"))
random.seed(60)


def ant_colony_optimization(salesman_number):
    # Choose parameters
    number_of_ants = 10
    number_of_iterations = 50
    evaporation_rate = 0.5
    alpha = 1
    beta = 1

    # Initialize the pheromone matrix
    pheromone_deposit = np.ones((n, n))

    # cities random coordinates
    cities = np.random.rand(n, 2)

    # Divide cities to subsets according to salesman_number
    for i in range(n):
        cities[i][0] = float(random.randint(0 + salesman_number, 100 + salesman_number)) / 100

    # Verifying if cities are properly divided
    print(salesman_number)
    print(cities)

    # Calculate distance matrix of cities
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i, j] = np.sqrt((cities[i, 0] - cities[j, 0]) ** 2 + (cities[i, 1] - cities[j, 1]) ** 2)

    # Probability of choosing city j
    def calculate_probability(i, j):
        return (pheromone_deposit[i, j] ** alpha) * ((1 / distance_matrix[i, j]) ** beta)

    # Next city to visit for an ant
    def calculate_next_city(current_city, visited_cities):
        unvisited_cities = [city for city in range(n) if city not in visited_cities]
        probabilities = [calculate_probability(current_city, city) for city in unvisited_cities]
        probabilities = probabilities / sum(probabilities)
        next_city = np.random.choice(unvisited_cities, p=probabilities)
        return next_city

    # Calculate the length of a tour
    def calculate_tour_length(tour):
        length = 0
        for i in range(n):
            j = (i + 1) % n
            length += distance_matrix[tour[i], tour[j]]
        return length

    # Initialize the best_tour to None as there is not one found yet
    # and best_tour_length to infinity
    best_tour = None
    best_tour_length = np.inf

    # Main loop of executing the Ant Colony Optimization
    # according to the number of iterations
    for iteration in range(number_of_iterations):
        # Initialize the tours of the ants
        tours = np.zeros((number_of_ants, n), dtype=int)

        # Each ant starts from a random city
        # This loop is for each ant
        for ant in range(number_of_ants):
            current_city = np.random.randint(n)
            visited_cities = [current_city]

            # Build the tour by choosing the next city to visit
            for step in range(n - 1):
                next_city = calculate_next_city(current_city, visited_cities)
                visited_cities.append(next_city)
                current_city = next_city

            # Remove start city and append it at end to complete the tour
            visited_cities.append(visited_cities[0])
            visited_cities.pop(0)

            # Store the tour of the ant
            tours[ant] = visited_cities

        # Update global pheromone matrix
        delta_pheromone_deposit = np.zeros((n, n))
        for ant in range(number_of_ants):
            tour = tours[ant]
            tour_len = calculate_tour_length(tour)
            for i in range(n):
                j = (i + 1) % n
                delta_pheromone_deposit[tour[i], tour[j]] += 1 / tour_len
                delta_pheromone_deposit[tour[j], tour[i]] += 1 / tour_len

        pheromone_deposit = (1 - evaporation_rate) * pheromone_deposit + delta_pheromone_deposit

    # Check if best tour is improved
    for ant in range(number_of_ants):
        tour = tours[ant]
        tour_leng = calculate_tour_length(tour)
        if tour_leng < best_tour_length:
            best_tour = tour[:-1]  # Eliminate Last (repeated) city
            best_tour_length = tour_leng

    print("Distance Matrix:")
    for i in range(n):
        for j in range(n):
            print("{:.2f}".format(distance_matrix[i, j]), end=" ")
        print()

    # Salesman start from
    start = list(set(tour) - set(best_tour))
    print("Salesperson started from node", start)

    # Output the final best tour
    if best_tour is not None:
        print("\nFinal best tour:", best_tour, "Length:", best_tour_length)
    else:
        print("\nNo best tour found.")

    return cities, best_tour, start

# Track the timme Taken
import time
start_time = time.time()

salesman1_cities, salesman1_best_tour, salesman1_start = ant_colony_optimization(0)
salesman2_cities, salesman2_best_tour, salesman2_start = ant_colony_optimization(100)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# Vizualization
unreached_x_1 = [i[0] for i in salesman1_cities]
unreached_y_1 = [i[1] for i in salesman1_cities]
reached_x_1 = []
reached_y_1 = []

unreached_x_2 = [i[0] for i in salesman2_cities]
unreached_y_2 = [i[1] for i in salesman2_cities]
reached_x_2 = []
reached_y_2 = []

fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("CARR Productions")
plt.suptitle("CS5800 - MTSP - Spring'23 - Ant Colony Optimization Algorithim")
plt.title("By CARR")
driver_1, = ax.plot(salesman1_cities[salesman1_start, 0], salesman1_cities[salesman1_start, 1], color='blue',
                    marker='^', linestyle='None')
driver_2, = ax.plot(salesman2_cities[salesman2_start, 0], salesman2_cities[salesman2_start, 1], color='yellow',
                    marker='^', linestyle='None')

points_targets_unreached_1, = ax.plot(unreached_x_1, unreached_y_1, color="red", marker='o', linestyle='None')
points_targets_reached_1, = ax.plot(reached_x_1, reached_y_1, color="green", marker='x', linestyle='None')

points_targets_unreached_2, = ax.plot(unreached_x_2, unreached_y_2, color="red", marker='o', linestyle='None')
points_targets_reached_2, = ax.plot(reached_x_2, reached_y_2, color="green", marker='x', linestyle='None')

i = 0
while (len(unreached_x_1) > 0 or len(unreached_x_2) > 0):
    if (len(unreached_x_1) > 0):
        reached_x_1.append(salesman1_cities[i, 0])
        reached_y_1.append(salesman1_cities[i, 1])
        unreached_x_1.remove(salesman1_cities[i, 0])
        unreached_y_1.remove(salesman1_cities[i, 1])
        points_targets_unreached_1.set_data(unreached_x_1, unreached_y_1)
        points_targets_reached_1.set_data(reached_x_1, reached_y_1)
        driver_1.set_data(salesman1_cities[i, 0], salesman1_cities[i, 1])
    if (len(unreached_x_2) > 0):
        reached_x_2.append(salesman2_cities[i, 0])
        reached_y_2.append(salesman2_cities[i, 1])
        unreached_x_2.remove(salesman2_cities[i, 0])
        unreached_y_2.remove(salesman2_cities[i, 1])
        points_targets_unreached_2.set_data(unreached_x_2, unreached_y_2)
        points_targets_reached_2.set_data(reached_x_2, reached_y_2)
        driver_2.set_data(salesman2_cities[i, 0], salesman2_cities[i, 1])
    plt.pause(1)
    i += 1

plt.show(block=True)