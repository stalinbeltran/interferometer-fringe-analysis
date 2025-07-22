
import numpy as np

a = np.array([[ 0, 40,  0,  52,  0, 55],
    [ 0, 41,  0,  53,  0, 53],
])

print(a)
a = a.reshape((12))
print(a)
a = a.reshape((6, 2))
print(a)
a = a[:, 1]
print(a)