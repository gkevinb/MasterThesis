import matplotlib.pyplot as plt
import scipy
from modules import timeseries
import scipy.stats
import numpy as np
import math


size = 100
x = scipy.arange(size)
# FIX NAMING CONVENTION LOGNORM OR LOGNORMAL!!! AND LOOK INTO OTHER ONES AS WELL!!!!
#y = timeseries._generate_numbers(['LOGNORMAL', 5, 2], size)
y = timeseries._generate_numbers(['NORMAL', 15, 2], size)

#y = timeseries._generate_numbers(['EXP', 1/5], size)
#y = timeseries._generate_numbers(['WEIBULL', 60, 10], size)
#y = timeseries._generate_numbers(['WEIBULL', 10, 8], size)


'''
# creating the dummy sample (using beta distribution)
# creating the histogram
h = plt.hist(y, bins=range(48))
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


def p_value_if_norm(samples):
    results = scipy.stats.kstest(samples, 'norm', scipy.stats.norm.fit(samples))
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


def get_normal_parameters(parameters):
    return [parameters[0], parameters[1]]


def determine_distribution(samples):
    p_values = dict()

    p_values['EXP'] = p_value_if_exp(samples)
    p_values['LOGNORM'] = p_value_if_lognorm(samples)
    p_values['WEIBULL'] = p_value_if_weibull(samples)
    p_values['NORMAL'] = p_value_if_norm(samples)

    print('P values: ' + str(p_values))
    p_values = possible_distributions(p_values)
    print('P values: ' + str(p_values))

    best_fit_distribution = []

    if len(p_values) > 1:
        if 'LOGNORM' in p_values.keys() and 'NORMAL' in p_values.keys():
            del p_values['LOGNORM']
            print('Deleting LOGNORM...')
        if 'WEIBULL' in p_values.keys() and 'EXP' in p_values.keys():
            del p_values['WEIBULL']
            print('Deleting WEIBULL...')

    if len(p_values) == 1:
        distribution = p_values.popitem()
        # Name of distribution
        best_fit_distribution.append(distribution[0])
        if distribution[0] == 'EXP':
            best_fit_distribution.extend(get_exp_parameters(scipy.stats.expon.fit(samples)))

        if distribution[0] == 'LOGNORM':
            best_fit_distribution.extend(get_lognorm_parameters(scipy.stats.lognorm.fit(samples)))

        if distribution[0] == 'WEIBULL':
            best_fit_distribution.extend(get_weibull_parameters(scipy.stats.weibull_min.fit(samples)))

        if distribution[0] == 'NORMAL':
            best_fit_distribution.extend(get_normal_parameters(scipy.stats.norm.fit(samples)))
    else:
        best_fit_distribution.append('UNIDENTIFIED DISTRIBUTION')

    return best_fit_distribution

# Able to determine the above shown distribution from samples. However weibull cannot be identified sometimes.
# And sometimes exp is identified as both exp and weibull since exp is a weibull with a beta of 1.
# Fix these.
# Lognorm seems to work all the time, more testing though
# Sometimes with low sample size, even 1000 is low enough, LOGNORM, WEIBULL, and NORMAL are all identified,
# when it should be NORMAL


def calculate_mttf_of(distribution):
    mttf = 0
    if distribution[0] == 'NORMAL':
        mttf = distribution[1]
    if distribution[0] == 'EXP':
        mttf = distribution[1]
    if distribution[0] == 'LOGNORM':
        mu = distribution[1]
        sigma = distribution[2]
        mttf = math.exp(mu + (0.5 * sigma ** 2))
    if distribution[0] == 'WEIBULL':
        scale = distribution[1]
        shape = distribution[2]
        mttf = scale * math.gamma(1 / shape + 1)

    return mttf


d = determine_distribution(y)
d = rel_weibull_dist = ['WEIBULL', 10, 8]
d = ['LOGNORM', 5, 2]
print(d)
print(calculate_mttf_of(d))