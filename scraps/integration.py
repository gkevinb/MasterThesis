from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import expon, norm, weibull_min, lognorm


x = np.linspace(0, 100, 1000)
print(x)
lambda_ = 1/5
y = 1 - expon.cdf(x, scale=1/lambda_)
y_int = integrate.cumtrapz(y, x, initial=0)
plt.plot(x, y_int, 'r-', x, y, 'b-')

print(y_int)


plt.show()