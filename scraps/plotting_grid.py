import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
import seaborn as sns


linspace = np.linspace(0, 10, 100)
x = 2 * linspace

fig, subplots = plt.subplots(2, 2, figsize=(7, 7))
subplots[0][0].plot(linspace, x)
subplots[0][1].plot(linspace, 2 * x)
subplots[1][0].plot(linspace, 3 * x)
subplots[1][1].plot(linspace, 4 * x)
plt.show()