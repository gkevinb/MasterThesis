from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
import math


def differentiate(x, y):
    #dy = np.zeros(y.shape, np.float)
    dy = np.zeros(len(y), np.float)
    dy[0:-1] = np.diff(y) / np.diff(x)
    dy[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
    return dy


y = np.linspace(0, 10, 10)
x = []
for _ in y:
    x.append(math.sqrt(_))
print(x)
print(y)

dy_ = differentiate(x, y)
print(dy_)

plt.plot(x, y, 'r-', x, dy_, 'b-')

plt.show()


