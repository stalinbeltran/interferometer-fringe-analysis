
import numpy as np

a = np.array([[ 0, 40,  0,  52,  0, 55],
    [ 0, 41,  0,  53,  0, 53],
])

def to8bits(a):
    a = a.reshape((6, 2))
    a = a[:, 1]
    return a
    

print(a)
a = to8bits(a)
print(a)
