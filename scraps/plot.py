import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np


def calculate_pdf(distribution, linspace):
    if distribution[0] == 'EXP':
        lambda_ = distribution[1]
        scale_ = 1 / lambda_
        return expon.pdf(linspace, scale=scale_)

    if distribution[0] == 'WEIBULL':
        scale = distribution[1]
        shape = distribution[2]
        return weibull_min.pdf(linspace, shape, loc=0, scale=scale)

    if distribution[0] == 'NORMAL':
        mu = distribution[1]
        sigma = distribution[2]
        return norm.pdf(linspace, loc=mu, scale=sigma)

    if distribution[0] == 'LOGNORM':
        mu = distribution[1]
        sigma = distribution[2]
        scale = math.exp(mu)
        return lognorm.pdf(linspace, sigma, loc=0, scale=scale)


def calculate_cdf(distribution, linspace):
    if distribution[0] == 'EXP':
        lambda_ = distribution[1]
        scale_ = 1 / lambda_
        return expon.cdf(linspace, scale=scale_)

    if distribution[0] == 'WEIBULL':
        scale = distribution[1]
        shape = distribution[2]
        return weibull_min.cdf(linspace, shape, loc=0, scale=scale)

    if distribution[0] == 'NORMAL':
        mu = distribution[1]
        sigma = distribution[2]
        return norm.cdf(linspace, loc=mu, scale=sigma)

    if distribution[0] == 'LOGNORM':
        mu = distribution[1]
        sigma = distribution[2]
        scale = math.exp(mu)
        return lognorm.cdf(linspace, sigma, loc=0, scale=scale)


fig, subplots = plt.subplots(1, 1, figsize=(6, 5))

lin_space = np.linspace(0, 10, 100)
a = np.empty(100)
a.fill(0.5)
theoretical_pdf = calculate_pdf(['EXP', 0.5], lin_space)
theoretical_cdf = calculate_cdf(['EXP', 0.5], lin_space)
subplots.plot(lin_space, a, 'r-', lw=1.5, alpha=0.6, label='Theoretical')
subplots.set_xlabel('x')
#subplots.set_ylabel('P(x)')
#subplots.set_ylabel('P(X\u2264x)')
subplots.set_ylim([0, 1])
subplots.set_ylabel('\u03BB(x)')

plt.show()

