from util import stochastic_round, waterfilling

import numpy as np
import math
from collections import defaultdict
import matplotlib.pyplot as plt

def debug(s):
    debug_on = False
    if(debug_on):
        print(s)

class Flow:
    def __init__(self, id, RTT, resources_used):
        self.id = id
        self.RTT = RTT
        self.resources_used = resources_used

class WorldModel:
    def __init__(self, users, resource_capacities):
        self.users = users
        self.resources = resource_capacities
        # Use users .resources_used to create the incidence matrix
        self.incidence_matrix = np.zeros((len(users), len(resource_capacities)))
        for i, user in enumerate(users):
            for resource in user.resources_used:
                j = list(resource_capacities.keys()).index(resource)
                self.incidence_matrix[i][j] = 1

        self.callback = None

    def register_callback(self, callback):
        self.callback = callback

    def run(self, init_n, n_rounds = 1000):
        n = init_n.copy()
        for i in range(n_rounds):
            print(f"\n### Iteration: {i} ###")
            tput = self.tput(n)
            n = self.callback(tput).copy()

    def tput(self, n):
        # debug(f"n: {n}")
        # debug(f"Weights: {weights}")
        # debug(f"Resources: {self.resources}")
        # debug(f"Incidence Matrix: {self.incidence_matrix}")
        weights = [n[i]/self.users[i].RTT for i in range(len(n))]
        return waterfilling(weights, self.resources, self.incidence_matrix)


class Optimizer:
    def __init__(self, users, resources, operator_weights):
        self.users = users
        self.resources = resources
        self.operator_weights = operator_weights

        # Construct a map from each resource to the users that use it
        self.resource_users = defaultdict(list)
        for i, user in enumerate(users):
            for resource in user.resources_used:
                self.resource_users[resource].append(i)

        # # No Access
        # - resource caps

    def set_decision(self, decision):
        self.n = decision

    def get_decision(self):
        return self.n

    def update(self, new_throughput):
        n = self.n.copy()

        print(n)
        if(sum(n) <= 1000):
            # Double all connections
            print("DOUBLE")
            return [x+2 for x in n]

        # Construct usage allocation for each user
        usage = [new_throughput[i]/self.operator_weights[i] for i in range(len(self.users))]

        print(self.resource_users)
        for resource, users_on_resource in self.resource_users.items():
            print(f"resource: {resource}")
            print(f"users_on_resource: {users_on_resource}")

            # Find the user on the resource with the highest usage
            max_user = max(users_on_resource, key=lambda user: usage[user])
            print(f"max_user: {max_user}")

            # Reduce the number of connections for the max user
            if (n[max_user] >= 2):
                # n[max_user] -= math.ceil(math.sqrt(n[max_user]))
                # n[max_user] -= 3
                n[max_user] -= math.ceil(n[max_user]*0.02)
        return n


def display(throughputs, goal):
    """
    supported values are '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
    """
    # Display the throughputs as three separate lines on a curve
    plt.plot(throughputs, marker='o', linestyle='None', markersize=0.5)

    # As well as the expected throughputs
    for i in range(len(goal)):
        plt.axhline(y=goal[i], color=f'C{i}', linestyle=':', label='Goal {i}')

    plt.show()

def regret(throughputs, actual):
    def error(throughput, actual):
        """
        Euclidean distance between throughput vector and actual vector
        """
        return math.sqrt(sum((throughput[i] - actual[i])**2 for i in range(len(throughput))))

    # Sum of errors for each slice in throughputs, comparing throughputs[i] to actual
    return sum(error(throughputs[i], actual) for i in range(len(throughputs)))


def simulate(world, optimizer, expected_throughputs):
    print("Starting Simulation")

    # Initialize Number of Connections
    n = [1,1,1]
    optimizer.set_decision(n)

    # Run the simulation for 2000 iterations
    throughput_history = []

    def xts_callback(throughput):
        # 1. WorldModel maps n -> tput.
        throughput_history.append(throughput)
        print("Throughput: ", throughput)

        # 2. Optimizer maps tput -> n.
        n = optimizer.update(throughput)
        optimizer.set_decision(n)

        print(f"outside n: {n}")
        return n

    world.register_callback(xts_callback)

    world.run(n)


    display(throughput_history, list(expected_throughputs.values()))
    regret_value = regret(throughput_history, list(expected_throughputs.values()))
    print(f"regret_value: {regret_value}")


def main():
    pass


if __name__ == "__main__":
    main()
