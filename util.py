import random 

# Stochastic Rounding of any number into floor(x) and ceil(x) 
def stochastic_round(x):
    floor_x = int(x)
    ceil_x = floor_x + 1
    if (random.random() < (x - floor_x)):
        return ceil_x
    else:
        return floor_x