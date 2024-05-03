from simulation_main import simulate, Flow, WorldModel, Optimizer
import numpy as np 
from util import waterfilling

def test_0():
    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 3, ["R1"]),
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.1, ["R2", "R3"]),
    ]
    resource_capacities = {
        'R1': 10,
        'R2': 4,
        'R3': 1,
    }

    operator_weights = [9, 1, 1]
    expected_throughputs = {
        'A': 9,
        'B': 1,
        'C': 1,
    }

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

def test_1():
    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 3, ["R1"]),
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.1, ["R2", "R3"]),
    ]
    resource_capacities = {
        'R1': 10,
        'R2': 4,
        'R3': 1,
    }

    operator_weights = [4, 1, 1]
    expected_throughputs = {
        'A': 8,
        'B': 2,
        'C': 1,
    }

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)


def test_2():
    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 10, ["R1"]),
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.5, ["R2"]),
    ]
    resource_capacities = {
        'R1': 100,
        'R2': 10,
    }

    operator_weights = [1, 1, 1]
    expected_throughputs = {
        'A': 95,
        'B': 5,
        'C': 5,
    }

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

def test_3():
    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 10, ["R1"]),
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.5, ["R2"]),
    ]
    resource_capacities = {
        'R1': 100,
        'R2': 10,
    }

    operator_weights = [24, 1, 1]
    expected_throughputs = {
        'A': 96,
        'B': 4,
        'C': 6,
    }

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

def test_4():
    """
    Test Case with 7 flows and 4 resources
    """
    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 10, ["R1"]),
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.5, ["R2"]),
        Flow("D", 2, ["R3"]),
        Flow("E", 1, ["R3", "R4"]),
        Flow("F", 0.5, ["R4"]),
        Flow("G", 10, ["R1"]),
    ]
    resource_capacities = {
        'R1': 100,
        'R2': 10,
        'R3': 100,
        'R4': 20,
    }

    operator_weights = [1, 1, 1, 1, 1, 1, 1]
    expected_throughputs = waterfilling([1 for _ in users], resource_capacities, [[1 if resource in user.resources_used else 0 for resource in resource_capacities] for user in users])

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)   
    print("Expected Throughputs", expected_throughputs)



def test_medium():
    # medium test case with 20 flows and 10 resources

    users = [
        # Each flow's Name, RTT, and Resources Used:
        Flow("A", 10, ["R1"]), # Blue
        Flow("B", 1, ["R1", "R2"]),
        Flow("C", 0.5, ["R2"]),
        Flow("D", 2, ["R3"]),
        Flow("E", 1, ["R3", "R4"]),
        Flow("F", 0.5, ["R4"]),
        Flow("G", 10, ["R5"]),
        Flow("H", 1, ["R5", "R6"]),
        Flow("I", 0.5, ["R6"]),
        Flow("J", 2, ["R7"]),
        Flow("K", 1, ["R7", "R8"]),
        Flow("L", 0.5, ["R8"]),
        Flow("M", 10, ["R9"]),
        Flow("N", 1, ["R9", "R10"]),
        Flow("O", 0.5, ["R10"]),
        Flow("P", 2, ["R1"]),
        Flow("Q", 1, ["R1", "R2"]), # Brown
        Flow("R", 0.5, ["R2"]),
        Flow("S", 2, ["R3"]),
        Flow("T", 1, ["R3", "R4"]),
    ]

    resource_capacities = {
        'R1': 100,
        'R2': 10,
        'R3': 100,
        'R4': 10,
        'R5': 100,
        'R6': 10,
        'R7': 100,
        'R8': 10,
        'R9': 100,
        'R10': 10,
    }
    # resource_capacities = {
    #     'R1': 50,
    #     'R2': 40,
    #     'R3': 1000,
    #     'R4': 10,
    #     'R5': 20,
    #     'R6': 15,
    #     'R7': 400,
    #     'R8': 10,
    #     'R9': 30,
    #     'R10': 200,
    # }

    operator_weights = [1 for _ in users]
    expected_throughputs = waterfilling([1 for _ in users], resource_capacities, [[1 if resource in user.resources_used else 0 for resource in resource_capacities] for user in users])

    wm = WorldModel(users, resource_capacities)
    optimizer = Optimizer(users, list(resource_capacities.keys()), operator_weights)
    simulate(WorldModel=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)
    print("Expected Throughputs", expected_throughputs)


def main():
    test_medium()

if __name__ == "__main__":
    main()