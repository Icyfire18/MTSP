import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class Car(object):
    """
    Class responsible for checking distance & driving 
    towards the target with a distance of 0.2 at a iteration
    """
    def __init__(self, name, map_size):
        """
        Constructor to initialzie when object is called
        """
        self.name = name
        self.x = float(random.randint(0, map_size))
        self.y = float(random.randint(0, map_size))
        self.target = None

    def drive_to_target(self):
        """
        Moves self closer to current target for every iteration
        """
        if self.target is None:
            return

        if self.get_distance(self.target) < .2:
            self.target.reached = True
        else:
            self.x += (self.target.x - self.x) * .2
            self.y += (self.target.y - self.y) * .2

    def get_distance(self, target):
        """
        Return distance between self and any target object
        """
        x_squablue = pow((self.x - target.x), 2)
        y_squablue = pow((self.y - target.y), 2)

        return sqrt(x_squablue + y_squablue)



class Target(object):
    """
    Class responsible to randomize the x and y coordinates of targets
    """
    def __init__(self, map_size, reached=False):
        """
        Constructor to create class variables and initialize when object is created
        """
        self.x = float(random.randint(0, map_size))
        self.y = float(random.randint(0, map_size))
        self.reached = reached

class Tracker(object):
    """
    Class responsible for initializing Cars and targets and moving vehicles 
    """

    def __init__(self, no_of_target, map_size):
        """
        Constructor to initialize cars and their Targets
        """
        self.cars = [Car("blue", map_size), Car("yellow", map_size)]
        self.targets = list(set([Target(map_size) for i in range(no_of_target)]))
        self.job_complete = False

    def move_cars(self):
        """
        Brute force to find best targets for respective cars
        """

        # Check if all targets have been reached
        unreached_targets = [target for target in self.targets if target.reached is False]
        if len(unreached_targets) == 0:
            self.job_complete = True
            return

        # List of tuples: (car object, target object, distance)
        car_target_distance = []

        for car in self.cars:
            for target in unreached_targets:
                car_target_distance.append((car, target, car.get_distance(target)))

        # Sort by distance
        car_target_distance.sort(key=lambda x: x[2])

        next_moves = car_target_distance[:1]

        # To make sure two cars don't go to the same location
        for potential_move in car_target_distance:
            if potential_move[0] != next_moves[0][0]:
                if potential_move[1] != next_moves[0][1]:
                    next_moves.append(potential_move)
                    break
            else:
                continue

        for move in next_moves:
            move[0].target = move[1]
            move[0].drive_to_target()

class Vizualize(object):
    """
    Class responsible for plotting the Targets & movement of Cars 
    """

    def __init__(self, dispatch, map_size, window_title, super_title, title):
        """
        Takes a Tracker object & plots its current state.
        """
        self.dispatch = dispatch

        # Plot initialization for vizualization
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title(window_title) 
        plt.suptitle(super_title)
        plt.title(title)
        self.ax.set_xlim(-10, map_size)
        self.ax.set_ylim(-10, map_size)

        # Cars represented by points
        self.points_blue, = self.ax.plot(self.dispatch.cars[0].x, self.dispatch.cars[0].y, color='blue', marker='^', linestyle='None')

        self.points_yellow, = self.ax.plot(self.dispatch.cars[1].x, self.dispatch.cars[1].y, color='yellow', marker='^', linestyle='None')

        # Targets represented by points
        targets_x_coordinates = [target.x for target in self.dispatch.targets]
        targets_y_coordinates = [target.y for target in self.dispatch.targets]
        self.points_targets_unreached, = self.ax.plot(targets_x_coordinates, targets_y_coordinates, color="red", marker='o', linestyle='None')

        # No completed targets initially
        self.points_targets_reached, = self.ax.plot([], [], color="green", marker='x', linestyle='None')

    def update(self):
        """
        Updates plot as cars move and targets are reached
        """

        # Targets Unreached are plotted
        targets_unreached_x_coordinates = [target.x for target in self.dispatch.targets if target.reached is False]
        targets_unreached_y_coordinates = [target.y for target in self.dispatch.targets if target.reached is False]
        self.points_targets_unreached.set_data(targets_unreached_x_coordinates, targets_unreached_y_coordinates)

        # Targets Reached are plotted
        targets_reached_x_coordinates = [target.x for target in self.dispatch.targets if target.reached is True]
        targets_reached_y_coordinates = [target.y for target in self.dispatch.targets if target.reached is True]
        self.points_targets_reached.set_data(targets_reached_x_coordinates, targets_reached_y_coordinates)

        # Car Movements are plotted
        self.points_blue.set_data(np.cfloat(self.dispatch.cars[0].x), np.cfloat(self.dispatch.cars[0].y))
        self.points_yellow.set_data(np.cfloat(self.dispatch.cars[1].x), np.cfloat(self.dispatch.cars[1].y))

        # Gap to capture animation
        plt.pause(0.01)
        

def main():
    """
    1. This is the driver function which is used to control the flow 
    1. Creates an instance of the Tracker class responsible for tracking targets & moving cars 
    2. Creates an instance of the Vizualize class for plotting the Targets & movement of Cars
    3. Running in loop to move cars towards targets until all targets have been reached.
    """

    ## Initialize vriables
    random.seed(60)
    map_size = 50
    window_title = "CARR Productions"
    super_title = "CS5800 - MTSP - Spring'23 - Geeedy Algorithim"
    title = "By CARR"
    num_of_cities = int(input("Enter the Number of Cities: "))

    ## Time calcualtion
    import time
    start_time = time.time()


    ## Universe creation
    t = Tracker(num_of_cities, map_size)
    v = Vizualize(t, map_size+10, window_title, super_title, title)

    ## Loop to run until all the cities have been reached
    while t.job_complete is False:
        t.move_cars()
        v.update()
    print("\n\n")
    print("Process finished --- %s seconds ---" % (time.time() - start_time))
    
    ## Freeze the output
    plt.show(block=True)

main()
