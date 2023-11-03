from math import sqrt, pow
from operator import mul

def norm(vector):
        mag = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        if mag == 0:
            return vector
        else:
            unit_vector = [vector[0] / mag,
                        vector[1] / mag,
                        vector[2] / mag]
        
            return unit_vector
        

def extend(vector, length):
    v_length = sqrt(pow(vector[0], 2) + pow(vector[1], 2) + pow(vector[2], 2))

    extended = list(map(mul, vector, [length/v_length for i in range(len(vector))]))

    return extended