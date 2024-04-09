from simulation_main import simulate, Flow, WorldModel, Optimizer

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
    simulate(world=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

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
    simulate(world=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)


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
    simulate(world=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

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
    simulate(world=wm, optimizer=optimizer, expected_throughputs=expected_throughputs)

def main():
    test_3()

if __name__ == "__main__":
    main()
