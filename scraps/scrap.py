import itertools
import random
import math
from modules import logicgate, timeseries

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

# Gamma function
print(math.gamma(4))
gamma = math.gamma(1/beta + 1)
mttf = nu * gamma
print(mttf)
exp = timeseries._generate_numbers(['EXP', 1/5], 1)
print(exp)
weibull = timeseries._generate_numbers(['WEIBULL', nu, beta], 1)
print(weibull)
