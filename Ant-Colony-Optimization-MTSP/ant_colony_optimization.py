import numpy as np
import matplotlib.pyplot as plt
import random

# Number of cities (input from user)
n = int(input("Enter the number of cities per salesman:"))


def ant_colony(salesman_no):

    # Generate random coordinates for cities
    cities = np.random.rand(n, 2)

    #salesman_no
    for i in range(n):
        cities[i][0] = float(random.randint(0+salesman_no, 100+salesman_no))/100

    print(salesman_no)
    print(cities)

    # Define the distance matrix
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.sqrt((cities[i, 0] - cities[j, 0])**2 + (cities[i, 1] - cities[j, 1])**2)


    # Define the parameters for the Ant Colony Optimization algorithm
    n_ants = 10
    n_iterations = 50
    evaporation_rate = 0.5
    alpha = 1
    beta = 1

    # Initialize the pheromone matrix
    pheromones = np.ones((n, n))

    # Define a function to calculate the probability of moving from city i to city j
    def probability(i, j):
        return (pheromones[i, j]**alpha) * ((1 / distances[i, j])**beta)

    # Define a function to choose the next city to visit for an ant
    def choose_next_city(current_city, visited_cities):
        unvisited_cities = [city for city in range(n) if city not in visited_cities]
        probabilities = [probability(current_city, city) for city in unvisited_cities]
        probabilities = probabilities / sum(probabilities)
        next_city = np.random.choice(unvisited_cities, p=probabilities)
        return next_city

    # Define a function to calculate the length of a tour
    def tour_length(tour):
        length = 0
        for i in range(n):
            j = (i + 1) % n
            length += distances[tour[i], tour[j]]
        return length

    # Initialize the best tour and its length
    best_tour = None
    best_tour_length = np.inf

    # Main loop of the Ant Colony Optimization algorithm
    for iteration in range(n_iterations):
        # Initialize the tours of the ants
        tours = np.zeros((n_ants, n), dtype=int)

        # Let each ant start from a random city
        for ant in range(n_ants):
            current_city = np.random.randint(n)
            visited_cities = [current_city]

            # Build the tour by choosing the next city to visit
            for step in range(n - 1):
                next_city = choose_next_city(current_city, visited_cities)
                visited_cities.append(next_city)
                current_city = next_city

            visited_cities.append(visited_cities[0])
            # Remove the starting city to complete the tour
            visited_cities.pop(0)

            # Store the tour of the ant
            tours[ant] = visited_cities

        # Update the pheromone matrix with the tours of the ants
        delta_pheromones = np.zeros((n, n))
        for ant in range(n_ants):
            tour = tours[ant]
            tour_len = tour_length(tour)  # <-- rename variable
            for i in range(n):
                j = (i + 1) % n
                delta_pheromones[tour[i], tour[j]] += 1 / tour_len  # <-- use renamed variable
                delta_pheromones[tour[j], tour[i]] += 1 / tour_len  # pheromones matrix is symmetric
        
        pheromones = (1 - evaporation_rate) * pheromones + delta_pheromones
        
    # Check if the best tour has been improved
    for ant in range(n_ants):
        tour = tours[ant]
        tour_leng = tour_length(tour)
        if tour_leng < best_tour_length:
            best_tour = tour[:-1] # Remove the last (repeated) city
            best_tour_length = tour_leng


    # Print the distance matrix
    print("Distance Matrix:")
    for i in range(n):
        for j in range(n):
            print("{:.2f}".format(distances[i, j]), end=" ")
        print()

    #Salesman start from
    start = list(set(tour) - set(best_tour))
    print("Salesperson started from node", start)


    #Output the final best tour
    if best_tour is not None:
        print("\nFinal best tour:", best_tour, "Length:", best_tour_length)
    else:
        print("\nNo best tour found.")

    return cities, best_tour, start 


salesman1_cities, salesman1_best_tour, salesman1_start = ant_colony(0)
salesman2_cities, salesman2_best_tour, salesman2_start = ant_colony(100)

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
driver_1, = ax.plot(salesman1_cities[salesman1_start,0], salesman1_cities[salesman1_start,1], color='blue', marker='^', linestyle='None')
driver_2, = ax.plot(salesman2_cities[salesman2_start,0], salesman2_cities[salesman2_start,1], color='yellow', marker='^', linestyle='None')


points_targets_unreached_1, = ax.plot(unreached_x_1, unreached_y_1, color="red", marker='o', linestyle='None')
points_targets_reached_1, = ax.plot(reached_x_1, reached_y_1, color="green", marker='x', linestyle='None')

points_targets_unreached_2, = ax.plot(unreached_x_2, unreached_y_2, color="red", marker='o', linestyle='None')
points_targets_reached_2, = ax.plot(reached_x_2, reached_y_2, color="green", marker='x', linestyle='None')

i=0
while (len(unreached_x_1)>0 or len(unreached_x_2)>0):
    if (len(unreached_x_1)>0):
        reached_x_1.append(salesman1_cities[i,0])
        reached_y_1.append(salesman1_cities[i,1])
        unreached_x_1.remove(salesman1_cities[i,0])
        unreached_y_1.remove(salesman1_cities[i,1])
        points_targets_unreached_1.set_data(unreached_x_1, unreached_y_1)
        points_targets_reached_1.set_data(reached_x_1, reached_y_1)
        driver_1.set_data(salesman1_cities[i,0], salesman1_cities[i,1])
    if(len(unreached_x_2)>0):
        reached_x_2.append(salesman2_cities[i,0])
        reached_y_2.append(salesman2_cities[i,1])
        unreached_x_2.remove(salesman2_cities[i,0])
        unreached_y_2.remove(salesman2_cities[i,1])
        points_targets_unreached_2.set_data(unreached_x_2, unreached_y_2)
        points_targets_reached_2.set_data(reached_x_2, reached_y_2)
        driver_2.set_data(salesman2_cities[i,0], salesman2_cities[i,1])
    plt.pause(1)
    i+=1
  
plt.show(block=True)