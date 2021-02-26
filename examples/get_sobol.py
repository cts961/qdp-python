from external.sobol import *
import numpy as np

rand = i4_sobol_generate(33, int(1e2), 2)


# rand2 = i4_sobol_generate(1, int(1e5), 0)
print(rand)

# np.random.rand()
# print(np.mean(rand2))