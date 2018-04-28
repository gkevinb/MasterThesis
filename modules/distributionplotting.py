import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
import seaborn as sns


def plot_exp(name, metric, distribution, times):
    lambda_ = distribution[1]
    scale_ = 1/lambda_

    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    linspace = np.linspace(expon.ppf(0.001, scale=scale_), expon.ppf(0.999, scale=scale_), 1000)

    subplots[0].plot(linspace, expon.pdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='exp pdf')
    subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Exponential PDF')

    subplots[1].plot(linspace, expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='exp cdf')
    subplots[1].set_title('Exponential CDF')

    subplots[2].plot(linspace, 1 - expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label=metric)
    subplots[2].set_title(metric)

    plt.show(block=False)


def plot_normal(name, metric, distribution, times):
    mu = distribution[1]
    sigma = distribution[2]

    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    linspace = np.linspace(norm.ppf(0.001, loc=mu, scale=sigma), norm.ppf(0.999, loc=mu, scale=sigma), 1000)

    subplots[0].plot(linspace, norm.pdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label='normal pdf')
    subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Normal PDF')

    subplots[1].plot(linspace, norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label='normal cdf')
    subplots[1].set_title('Normal CDF')

    subplots[2].plot(linspace, 1 - norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6, label=metric)
    subplots[2].set_title(metric)

    plt.show(block=False)


def plot_weibull(name, metric, distribution, times):
    scale = distribution[1]
    shape = distribution[2]

    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    linspace = np.linspace(weibull_min.ppf(0.001, shape, loc=0, scale=scale),
                           weibull_min.ppf(0.999, shape, loc=0, scale=scale), 1000)

    subplots[0].plot(linspace, weibull_min.pdf(linspace, shape, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='weibull pdf')
    subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Weibull PDF')

    subplots[1].plot(linspace, weibull_min.cdf(linspace, shape, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='weibull cdf')
    subplots[1].set_title('Weibull CDF')

    subplots[2].plot(linspace, 1 - weibull_min.cdf(linspace, shape, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label=metric)
    subplots[2].set_title(metric)

    plt.show(block=False)


def plot_lognorm(name, metric, distribution, times):
    # s = sigma and scale = exp(mu).
    mu = distribution[1]
    sigma = distribution[2]
    scale = math.exp(mu)

    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    linspace = np.linspace(lognorm.ppf(0.001, sigma, loc=0, scale=scale),
                           lognorm.ppf(0.999, sigma, loc=0, scale=scale), 1000)

    subplots[0].plot(linspace, lognorm.pdf(linspace, sigma, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='lognormal pdf')
    subplots[0].hist(times, bins=50, normed=True, histtype='stepfilled', alpha=0.2)
    subplots[0].set_title('Lognormal PDF')

    subplots[1].plot(linspace, lognorm.cdf(linspace, sigma, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label='normal cdf')

    subplots[1].set_title('Lognormal CDF')

    subplots[2].plot(linspace, 1 - lognorm.cdf(linspace, sigma, loc=0, scale=scale),
                     'r-', lw=1, alpha=0.6, label=metric)
    subplots[2].set_title(metric)

    #plt.show()
    plt.show(block=False)


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
    subplots[2].set_title('Reliability')

    plt.show()
