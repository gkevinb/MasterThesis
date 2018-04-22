import matplotlib.pyplot as plt
import scipy
from modules import timeseries
import scipy.stats
import numpy as np


size = 10000
x = scipy.arange(size)
y = timeseries._generate_numbers(['LOGNORMAL', 5, 2], size)
#y = timeseries._generate_numbers(['EXP', 1/5], size)
#y = timeseries._generate_numbers(['WEIBULL', 60, 10], size)
# creating the dummy sample (using beta distribution)
# creating the histogram
h = plt.hist(y, bins=range(48))

'''
dist_names = ['lognorm', 'weibull_min', 'expon']

for dist_name in dist_names:
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(y)
    print('Parameters for ' + str(dist_name) + ' : ' + str(param))
    print(scipy.stats.kstest(y, 'weibull_min', scipy.stats.weibull_min.fit(y)))
    print(scipy.stats.kstest(y, 'expon', scipy.stats.expon.fit(y)))
    print(scipy.stats.kstest(y, 'lognorm', scipy.stats.lognorm.fit(y)))
    pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
    plt.plot(pdf_fitted, label=dist_name)
    plt.xlim(0, 47)
plt.legend(loc='upper left')
plt.show()

'''

def p_value_if_weibull(samples):
    results = scipy.stats.kstest(samples, 'weibull_min', scipy.stats.weibull_min.fit(samples))
    p_value = results[1]
    return p_value


def p_value_if_exp(samples):
    results = scipy.stats.kstest(samples, 'expon', scipy.stats.expon.fit(samples))
    p_value = results[1]
    return p_value


def p_value_if_lognorm(samples):
    results = scipy.stats.kstest(samples, 'lognorm', scipy.stats.lognorm.fit(samples))
    p_value = results[1]
    return p_value


def possible_distributions(p_values_dict):
    """
    Checks which distributions have p-value of at least 0.05,
    so it's possible the samples are from that distribution.
    :param p_values_dict:
    :return:
    """
    significant_p_values = dict()
    for distribution, p_val in p_values_dict.items():
        if p_val > 0.05:
            significant_p_values[distribution] = p_val

    return significant_p_values


def get_exp_parameters(parameters):
    return [1/parameters[1]]


def get_lognorm_parameters(parameters):
    return [np.log(parameters[2]), parameters[0]]


def get_weibull_parameters(parameters):
    return [parameters[2], parameters[0]]


p_values = dict()

p_values['EXP'] = p_value_if_exp(y)
p_values['LOGNORM'] = p_value_if_lognorm(y)
p_values['WEIBULL'] = p_value_if_weibull(y)

print('P values: ' + str(p_values))
p_values = possible_distributions(p_values)
print('P values: ' + str(p_values))

best_fit_distribution = []

if len(p_values) == 1:
    distribution = p_values.popitem()
    # Name of distribution
    best_fit_distribution.append(distribution[0])
    if distribution[0] == 'EXP':
        best_fit_distribution.extend(get_exp_parameters(scipy.stats.expon.fit(y)))

    if distribution[0] == 'LOGNORM':
        best_fit_distribution.extend(get_lognorm_parameters(scipy.stats.lognorm.fit(y)))

    if distribution[0] == 'WEIBULL':
        best_fit_distribution.extend(get_weibull_parameters(scipy.stats.weibull_min.fit(y)))


# Able to determine the above shown distribution from samples. However weibull cannot be identified sometimes.
# And sometimes exp is identified as both exp and weibull since exp is a weibull with a beta of 1.
# Fix these.
# Lognorm seems to work all the time, more testing though


print(best_fit_distribution)
