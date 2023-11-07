from math import sqrt, pow
from operator import mul, sub
from numpy import cross

def vnorm(vector):
    magnitude = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    if magnitude == 0:
        return vector
    else:
        unit_vector = [vector[0] / magnitude,
                       vector[1] / magnitude,
                       vector[2] / magnitude]
    
        return unit_vector

def vextend(vector, length):
    if vector is not None:
        v_length = sqrt(pow(vector[0], 2) + pow(vector[1], 2) + pow(vector[2], 2))

        extended = list(map(mul, vector, [length/v_length for i in range(len(vector))]))

        return extended
    return None

def vadd(a, b):
    if a is not None and b is not None:
        if len(a) != len(b):
            print(a)
            print(b)
            raise ValueError(f"dim a ({len(a)}) != dim b ({len(b)})")
        if len(a) == 3:
            return [a[0]+b[0], a[1]+b[1], a[2]+a[2]]
        if len(b) == 2:
            return [a[0]+b[0], a[1]+b[1]]
    return None
    
def calculate_face_normal(verts_dict, face):
    p1 = verts_dict[face[0]]
    p2 = verts_dict[face[1]]
    p3 = verts_dict[face[-2]]

    v1 = list(map(sub, p2, p1))
    v2 = list(map(sub, p3, p1))

    return cross(v1, v2)