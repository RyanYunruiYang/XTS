from util import waterfilling, stochastic_round

import numpy as np
import math
from collections import defaultdict
import matplotlib.pyplot as plt

def debug(s):
    debug_on = False
    if(debug_on):
        print(s)

class Flow:
    """
    Represents a flow in the network, with a unique ID, RTT, and resources used.
    """
    def __init__(self, id, RTT, resources_used):
        self.id = id
        self.RTT = RTT
        self.resources_used = resources_used

class WorldModel:
    """"
    Represents the world model, which maps the number of connections to the throughput.
    """
    def __init__(self, users, resource_capacities):
        self.users = users
        self.resources = resource_capacities
        # Use users .resources_used to create the incidence matrix
        self.incidence_matrix = np.zeros((len(users), len(resource_capacities)))
        for i, user in enumerate(users):
            for resource in user.resources_used:
                j = list(resource_capacities.keys()).index(resource)
                self.incidence_matrix[i][j] = 1

    def tput(self, n):
        weights = [n[i]/self.users[i].RTT for i in range(len(n))]
        return waterfilling(weights, self.resources, self.incidence_matrix)


class Optimizer:
    """
    FTS Optimizer Object. Controls the knob n, the number of connections for each user.
    """
    def __init__(self, users, resources, operator_weights):
        self.users = users
        self.resources = resources
        self.operator_weights = operator_weights

        # Construct a map from each resource to the users that use it
        self.resource_users = defaultdict(list)
        for i, user in enumerate(users):
            for resource in user.resources_used:
                self.resource_users[resource].append(i)

    def set_decision(self, decision):
        """"
        Set the decision for the optimizer, the number of connections for each user.
        """
        self.n = decision
    
    def get_decision(self):
        return self.n

    def update(self, new_throughput):
        """
        MAIN LOGIC OF OPTIMIZER. 
        Given the new throughput, update the number of connections.
        """
        n = self.n.copy()

        # Additive Increase
        if(sum(n) <= 200):
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
                # Different Update Algorithms: 
                # n[max_user] -= math.ceil(math.sqrt(n[max_user]))
                # n[max_user] -= 3

                alpha = 0.02
                # n[max_user] -= stochastic_round(n[max_user]*alpha)
                # n[max_user] -= math.ceil(n[max_user]*alpha)
                n[max_user] -= alpha * n[max_user]
        return n


def display(throughputs, goal):
    """
    Displays the throughput evolution vs. goal throughput.
    """    
    # Display the throughputs as three separate lines on a curve
    plt.plot(throughputs, marker='o', linestyle='None', markersize=0.5)
    
    # As well as the expected throughputs
    for i in range(len(goal)):
        plt.axhline(y=goal[i], color=f'C{i}', linestyle=':', label='Goal {i}')
        # Supported linestyles are:
        # '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'

    plt.show()

def display_one_by_one(throughputs, goal):
    """
    Displays the throughput evolution vs. goal throughput for each flow
    in a separate plot, each of which are shown one by one.
    """
    for i in range(len(throughputs[0])):
        plt.plot([throughput[i] for throughput in throughputs], marker='o', linestyle='None', markersize=0.5)
        plt.axhline(y=goal[i], color=f'C{i}', linestyle=':', label='Goal {i}')
        plt.show()

def regret(throughputs, actual):
    """
    Returns the regret of the throughputs, a list of throughput vector
    compared to the (single) expected throughput vector.
    """
    def error(throughput, actual):
        """
        Euclidean distance between throughput vector and actual vector
        """
        return math.sqrt(sum((throughput[i] - actual[i])**2 for i in range(len(throughput))))
    
    # Sum of errors for each slice in throughputs, comparing throughputs[i] to actual
    return sum(error(throughputs[i], actual) for i in range(len(throughputs)))

def avg_to_ideal(throughputs, actual):
    # Compute average throughput:
    avg = [sum(throughputs[i][j] for i in range(len(throughputs))) / len(throughputs) for j in range(len(throughputs[0]))]
    return avg, regret([avg], actual)


def simulate(WorldModel, optimizer, expected_throughputs):
    """
    Simulates the network, given the WorldModel and Optimizer objects.
    """
    print("Starting Simulation")

    # Initialize Number of Connections
    n = [1 for _ in WorldModel.users]
    optimizer.set_decision(n)

    # Run the simulation for 2000 iterations
    throughput_history = []
    for i in range(2000):
        print(f"\n### Iteration: {i} ###")

        # 1. WorldModel maps n -> tput.
        throughput = WorldModel.tput(n)
        throughput_history.append(throughput)
        print("Throughput: ", throughput)

        # 2. Optimizer maps tput -> n.
        n = optimizer.update(throughput)
        optimizer.set_decision(n)

        print(f"outside n: {n}")
    
    # Postprocessing
    if isinstance(expected_throughputs, dict):
        expected_throughputs = list(expected_throughputs.values())

    display(throughput_history, expected_throughputs)
    display_one_by_one(throughput_history, expected_throughputs)
    regret_value = regret(throughput_history, expected_throughputs)
    print(f"regret_value: {regret_value}")

    avg, avg_regret = avg_to_ideal(throughput_history, expected_throughputs)
    print(f"avg: {avg} error: {avg_regret}")


def main():
    pass


if __name__ == "__main__":
    main()