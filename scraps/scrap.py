import itertools
import random
import math
from modules import timeseries
import numpy as np
from scipy.stats import expon, lognorm, weibull_min
from scipy import stats
'''
p = {0, 1, 2}
children = [{0, 1}, {0, 2}, {1, 2}]
for x, y in itertools.permutations(children, 2):
    print(x, y)

print('----------------------------------')
for x in children:
    # Get another cut_set(_under_test) from cut_sets
    for y in children:
        # Check if the two cut_set are not the same
        if x != y:
            print(x, y)

print('----------------------------------')

# is_EVEN = lambda i: i % 2 == 0
# is_ODD = lambda i: i % 2 == 1


def is_EVEN(i): return i % 2 == 0


def is_ODD(i): return i % 2 == 1


print(is_EVEN(10))

'''
#print(random.weibullvariate(60, 100))
#print(random.expovariate(1/50))
#print(random.lognormvariate(5, 6))
nu = 60
beta = 10
print(random.weibullvariate(nu, beta))

# Calculate the MTTF of weibull equation
# Gamma function
print(math.gamma(4))
gamma = math.gamma(1/beta + 1)
mttf = nu * gamma
print(mttf)


size = 10000

exp = timeseries._generate_numbers(['EXP', 1/5], size)
print(exp)
weibull = timeseries._generate_numbers(['WEIBULL', nu, beta], size)
print(weibull)

lognormal = timeseries._generate_numbers(['LOGNORMAL', 5, 2], size)
print(lognormal)

# Calculate the MTTF of lognormal equation
ln_times = []
for x in lognormal:
    ln_times.append(np.log(x))
print(np.mean(ln_times))
print(np.std(ln_times))
print(lognorm.fit(lognormal))
print(weibull_min.fit(weibull))
print(expon.fit(exp))
undertest = exp
print(stats.kstest(undertest, 'expon', stats.expon.fit(undertest)))
print(stats.kstest(undertest, 'lognorm', stats.lognorm.fit(undertest)))
print(stats.kstest(undertest, 'weibull_min', stats.weibull_min.fit(undertest)))

