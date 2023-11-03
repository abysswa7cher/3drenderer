import numpy as np

projection = np.matrix([[1, 0, 0],
                        [0, 1, 0]])

x, y, z = [float(c) for c in input("enter point coords:").split(", ")]
point = np.matrix([[x], 
                   [y],
                   [z]])

def matmul(a, b):

    rows_a, cols_a = a.shape
    rows_b, cols_b = b.shape

    if cols_a != rows_b:
        raise ValueError(f"dim a ({len(a[0]) - 1}) != dim b ({len(b) - 1})")
    
    result = np.matrix([[0.0] for i in range(rows_a) for j in range(cols_b)])
    
    for i in range(rows_a):
        for j in range(cols_b):
            sum = 0

            for k in range(cols_a):
                sum += a[i, k] * b[k, j]
            result[i, j] = float(sum)

    return result
print(matmul(projection, point))