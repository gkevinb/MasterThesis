from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt


def differentiate(x, y):
    dy = np.zeros(y.shape, np.float)
    dy[0:-1] = np.diff(y) / np.diff(x)
    dy[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    return dy


x = np.linspace(0, 10, 100)
y = x ** 2

dy_ = differentiate(x, y)

plt.plot(x, y, 'r-', x, dy_, 'b-')

plt.show()


