import random 
import numpy as np 

def waterfilling(weights, resources, incidence_matrix):
    """
    Perform water-filling for Max-Min fairness.

    TODO: Handle weights = 0.
    """
    # Assert all weights are > 0
    assert all(weights[i] > 0 for i in range(len(weights)))

    user_weights = weights
    resource_caps = list(resources.values())

    allocation = [0 for i in range(len(weights))]
    available_resources = [resource_caps[i] for i in range(len(resources))]

    user_frozen = [False for i in range(len(weights))]
    resource_frozen = [False for i in range(len(resources))]

    while not all(user_frozen) and not all(resource_frozen):
        # 1. Compute resource_demand, the amount of load on each resource.
        resource_demand = [0 for i in range(len(resources))]
        for i in range(len(weights)): 
            for j in range(len(resources)):
                if (incidence_matrix[i][j] == 1):
                    if (not user_frozen[i]):
                        resource_demand[j] += user_weights[i]

        # 2. Compute next_resource_step, the biggest legal step that can be taken.
        next_resource_step = 0
        for i in range(len(resources)):
            if (available_resources[i] > 0 and resource_demand[i] > 0):
                ratio = available_resources[i]/resource_demand[i]
                if (ratio < next_resource_step or next_resource_step == 0):
                    next_resource_step = ratio

        # 3. Allocate the resources to the users, and propagate capacity changes to resources. 
        for i in range(len(weights)):
            if (not user_frozen[i]):
                allocation[i] += user_weights[i] * next_resource_step

                # For all resources that the user uses, subtract the demand
                for j in range(len(resources)):
                    if (incidence_matrix[i][j] == 1):
                        available_resources[j] -= user_weights[i] * next_resource_step

        # 4. Freeze all the resources which are empty.
        for i in range(len(resources)):
            if (abs(available_resources[i]) < 0.001):
                resource_frozen[i] = True
        # 5. Freeze all the users which use frozen resources.
        for i in range(len(weights)):
            for j in range(len(resources)):
                if (incidence_matrix[i][j] == 1 and resource_frozen[j]):
                    user_frozen[i] = True

    assert all(user_frozen)

    # Calculate resource usage on each resource, and assert it is less than capacity
    resource_util = [0 for i in range(len(resources))]
    for i in range(len(weights)):
        for j in range(len(resources)):
            if (incidence_matrix[i][j] == 1):
                resource_util[j] += allocation[i]
    assert all(resource_util[i] <= resource_caps[i]+0.000001 for i in range(len(resources)))     

    return allocation

# Stochastic Rounding of any number into floor(x) and ceil(x) 
def stochastic_round(x):
    """
    Samples from a disribution that always returns floor(x) or ceil(x)
    with mean x.
    """
    floor_x = int(x)
    ceil_x = floor_x + 1
    if (random.random() < (x - floor_x)):
        return ceil_x
    else:
        return floor_x