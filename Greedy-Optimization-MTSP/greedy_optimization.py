import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class Truck(object):
    """
    Class responsible for checking distance
    """
    def __init__(self, name):
        self.name = name
        self.x = float(random.randint(0, 50))
        self.y = float(random.randint(0, 50))
        self.target = None

    def drive_to_target(self):
        """
        Moves self closer to current target
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

    def __init__(self, reached=False):
        self.x = float(random.randint(0, 50))
        self.y = float(random.randint(0, 50))
        self.reached = reached

class Tracker(object):
    """
    Class responsible for tracking targets & moving trucks 
    """

    def __init__(self, no_of_target):
        self.trucks = [Truck("blue"), Truck("yellow")]
        self.targets = list(set([Target() for i in range(no_of_target)]))
        self.job_complete = False

    def move_trucks(self):
        """
        Brute force to find best targets for respective trucks
        """

        # Check if all targets have been reached
        unreached_targets = [target for target in self.targets if target.reached is False]
        if len(unreached_targets) == 0:
            self.job_complete = True
            return

        # List of tuples: (truck object, target object, distance)
        truck_target_distance = []

        for truck in self.trucks:
            for target in unreached_targets:
                truck_target_distance.append((truck, target, truck.get_distance(target)))

        # Sort by distance
        truck_target_distance.sort(key=lambda x: x[2])

        next_moves = truck_target_distance[:1]

        for potential_move in truck_target_distance:
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
    Class responsible for plotting the Targets & movement of Trucks 
    """

    def __init__(self, dispatch):
        """
        Takes a Tracker object & plots its current state.
        """
        self.dispatch = dispatch

        # Plot initialization for vizualization
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 60)
        self.ax.set_ylim(-10, 60)

        # Trucks represented by points
        self.points_blue, = self.ax.plot(self.dispatch.trucks[0].x, self.dispatch.trucks[0].y, color='blue', marker='^', linestyle='None')

        self.points_yellow, = self.ax.plot(self.dispatch.trucks[1].x, self.dispatch.trucks[1].y, color='yellow', marker='^', linestyle='None')

        # Targets represented by points
        targets_x_coordinates = [target.x for target in self.dispatch.targets]
        targets_y_coordinates = [target.y for target in self.dispatch.targets]
        self.points_targets_unreached, = self.ax.plot(targets_x_coordinates, targets_y_coordinates, color="red", marker='o', linestyle='None')

        # No completed targets initially
        self.points_targets_reached, = self.ax.plot([], [], color="green", marker='x', linestyle='None')

    def update(self):
        """
        Updates plot as trucks move and targets are reached
        """

        # Targets Unreached are plotted
        targets_unreached_x_coordinates = [target.x for target in self.dispatch.targets if target.reached is False]
        targets_unreached_y_coordinates = [target.y for target in self.dispatch.targets if target.reached is False]
        self.points_targets_unreached.set_data(targets_unreached_x_coordinates, targets_unreached_y_coordinates)

        # Targets Reached are plotted
        targets_reached_x_coordinates = [target.x for target in self.dispatch.targets if target.reached is True]
        targets_reached_y_coordinates = [target.y for target in self.dispatch.targets if target.reached is True]
        self.points_targets_reached.set_data(targets_reached_x_coordinates, targets_reached_y_coordinates)

        # Truck Movements are plotted
        self.points_blue.set_data(np.cfloat(self.dispatch.trucks[0].x), np.cfloat(self.dispatch.trucks[0].y))
        self.points_yellow.set_data(np.cfloat(self.dispatch.trucks[1].x), np.cfloat(self.dispatch.trucks[1].y))

        # Gap to capture animation
        plt.pause(0.01)
        

def main():
    """
    1. This is the driver function which is used to control the flow 
    1. Creates an instance of the Tracker class responsible for tracking targets & moving trucks 
    2. Creates an instance of the Vizualize class for plotting the Targets & movement of Trucks
    3. Running in loop to move trucks towards targets until all targets have been reached.
    """

    random.seed(60)
    num_of_cities = int(input("Enter the Number of Cities: "))
    t = Tracker(num_of_cities)
    v = Vizualize(t)

    while t.job_complete is False:
        t.move_trucks()
        v.update()
    
    plt.show(block=True)
main()
