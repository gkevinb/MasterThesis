import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
import seaborn as sns


EMPTY_LIST = []


def plot_exp(name, metric, distribution, times):
    lambda_ = distribution[1]
    scale_ = 1/lambda_

    num_of_subplots = 0
    figure_width = 10
    if metric == 'Reliability':
        num_of_subplots = 3
        figure_width = 13
    if metric == 'Maintainability':
        num_of_subplots = 2
        figure_width = 9

    fig, subplots = plt.subplots(1, num_of_subplots, figsize=(figure_width, 4))
    fig.suptitle(name)

    linspace = np.linspace(expon.ppf(0.001, scale=scale_), expon.ppf(0.999, scale=scale_), 1000)

    subplots[0].plot(linspace, expon.pdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='exp pdf')
    if times != EMPTY_LIST:
        subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Exponential PDF')

    subplots[1].plot(linspace, expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='exp cdf')
    if metric == 'Reliability':
        subplots[1].set_title('Exponential CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Exponential CDF (Maintainability)')

    if metric == 'Reliability':
        subplots[2].plot(linspace, 1 - expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label=metric)
        subplots[2].set_title(metric)

    plt.show()
    #plt.show(block=False)


def plot_normal(name, metric, distribution, times):
    mu = distribution[1]
    sigma = distribution[2]

    num_of_subplots = 0
    figure_width = 10
    if metric == 'Reliability':
        num_of_subplots = 3
        figure_width = 13
    if metric == 'Maintainability':
        num_of_subplots = 2
        figure_width = 9

    fig, subplots = plt.subplots(1, num_of_subplots, figsize=(figure_width, 4))
    fig.suptitle(name)

    linspace = np.linspace(norm.ppf(0.001, loc=mu, scale=sigma), norm.ppf(0.999, loc=mu, scale=sigma), 1000)

    subplots[0].plot(linspace, norm.pdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label='normal pdf')
    if times != EMPTY_LIST:
        subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Normal PDF')

    subplots[1].plot(linspace, norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label='normal cdf')
    if metric == 'Reliability':
        subplots[1].set_title('Normal CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Normal CDF (Maintainability)')

    if metric == 'Reliability':
        subplots[2].plot(linspace, 1 - norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label=metric)
        subplots[2].set_title(metric)

    plt.show()
    #plt.show(block=False)


def plot_weibull(name, metric, distribution, times):
    scale = distribution[1]
    shape = distribution[2]

    num_of_subplots = 0
    figure_width = 10
    if metric == 'Reliability':
        num_of_subplots = 3
        figure_width = 13
    if metric == 'Maintainability':
        num_of_subplots = 2
        figure_width = 9

    fig, subplots = plt.subplots(1, num_of_subplots, figsize=(figure_width, 4))
    fig.suptitle(name)

    linspace = np.linspace(weibull_min.ppf(0.001, shape, loc=0, scale=scale),
                           weibull_min.ppf(0.999, shape, loc=0, scale=scale), 1000)

    subplots[0].plot(linspace, weibull_min.pdf(linspace, shape, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='weibull pdf')
    if times != EMPTY_LIST:
        subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Weibull PDF')

    subplots[1].plot(linspace, weibull_min.cdf(linspace, shape, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='weibull cdf')
    subplots[1].set_title('Weibull CDF')
    if metric == 'Reliability':
        subplots[1].set_title('Weibull CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Weibull CDF (Maintainability)')

    if metric == 'Reliability':
        subplots[2].plot(linspace, 1 - weibull_min.cdf(linspace, shape, loc=0, scale=scale),
                         'r-', lw=1, alpha=0.6, label=metric)
        subplots[2].set_title(metric)

    plt.show()
    #plt.show(block=False)


def plot_lognorm(name, metric, distribution, times):
    # s = sigma and scale = exp(mu).
    mu = distribution[1]
    sigma = distribution[2]
    scale = math.exp(mu)

    num_of_subplots = 0
    figure_width = 10
    if metric == 'Reliability':
        num_of_subplots = 3
        figure_width = 13
    if metric == 'Maintainability':
        num_of_subplots = 2
        figure_width = 9

    fig, subplots = plt.subplots(1, num_of_subplots, figsize=(figure_width, 4))
    fig.suptitle(name)

    linspace = np.linspace(lognorm.ppf(0.001, sigma, loc=0, scale=scale),
                           lognorm.ppf(0.999, sigma, loc=0, scale=scale), 1000)

    subplots[0].plot(linspace, lognorm.pdf(linspace, sigma, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='lognormal pdf')
    if times != EMPTY_LIST:
        subplots[0].hist(times, bins=50, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Lognormal PDF')

    subplots[1].plot(linspace, lognorm.cdf(linspace, sigma, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='normal cdf')
    if metric == 'Reliability':
        subplots[1].set_title('Lognormal CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Lognormal CDF (Maintainability)')

    if metric == 'Reliability':
        subplots[2].plot(linspace, 1 - lognorm.cdf(linspace, sigma, loc=0, scale=scale),
                         'r-', lw=1, alpha=0.6, label=metric)
        subplots[2].set_title(metric)

    plt.show()
    #plt.show(block=False)


def plot_arbitrary_distribution(name, times):
    # Reliability for now
    # Maybe fix inconsistencies with the numbers on the axis
    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    sns.distplot(times, hist=True, ax=subplots[0])
    subplots[0].set_title('PDF')

    sns.kdeplot(times, cumulative=True, ax=subplots[1])
    subplots[1].set_title('CDF')

    times.sort()
    samples = len(times)
    one_minus_cdf = [1 - (x / samples) for x in range(1, samples + 1)]

    subplots[2].plot(times, one_minus_cdf)
    subplots[2].set_ylim([0, 1.05])
    # For comparing graphs
    #subplots[2].set_xlim([0, 100])
    subplots[2].set_title('Reliability')

    plt.show()


def plot_():
    fig, subplot = plt.subplots(1, 1)
    #lambda_ = distribution[1]
    #scale_ = 1 / lambda_
    linspace = np.linspace(0, 10, 1000)

    rel = (1 - expon.cdf(linspace, expon.pdf(linspace, scale=5)))
    print(rel)

    subplot.plot(linspace, rel)

    plt.show()
