import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
import seaborn as sns


EMPTY_LIST = []

def plot_exp(name, metric, distribution, times, theoretical_distribution=None):
    lambda_ = distribution[1]
    scale_ = 1/lambda_

    theoretical_scale = None
    # Checks whether there is a theoretical distribution to compare it to
    if theoretical_distribution is not None:
        theoretical_lambda = theoretical_distribution[1]
        theoretical_scale = 1/theoretical_lambda

    fig, subplots = setup_fig_subplots(metric)
    fig.suptitle(name)

    linspace = np.linspace(expon.ppf(0.001, scale=scale_), expon.ppf(0.999, scale=scale_), 1000)

    # First plot PDF
    if theoretical_distribution is not None:
        subplots[0].plot(linspace, expon.pdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='Reconstructed')
        subplots[0].plot(linspace, expon.pdf(linspace, scale=theoretical_scale), 'b-', lw=1, alpha=0.6,
                         label='Theoretical')
        subplots[0].legend()
    else:
        subplots[0].plot(linspace, expon.pdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6)

    if times != EMPTY_LIST:
        if metric == 'Reliability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to failures')
        if metric == 'Maintainability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to repairs')
        subplots[0].legend()
    subplots[0].set_title('Exponential PDF')


    # Second plot CDF and/or Maintainability
    if theoretical_distribution is not None:
        subplots[1].plot(linspace, expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6, label='Reconstructed')
        subplots[1].plot(linspace, expon.cdf(linspace, scale=theoretical_scale), 'b-', lw=1, alpha=0.6,
                         label='Theoretical')
        subplots[1].legend()
    else:
        subplots[1].plot(linspace, expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6)
    if metric == 'Reliability':
        subplots[1].set_title('Exponential CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Exponential CDF (Maintainability)')

    # Third plot Reliability
    if metric == 'Reliability':
        if theoretical_distribution is not None:
            subplots[2].plot(linspace, 1 - expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6,
                             label='Reconstructed')
            subplots[2].plot(linspace, 1 - expon.cdf(linspace, scale=theoretical_scale), 'b-', lw=1, alpha=0.6,
                             label='Theoretical')
            subplots[2].legend()
        else:
            subplots[2].plot(linspace, 1 - expon.cdf(linspace, scale=scale_), 'r-', lw=1, alpha=0.6)
        subplots[2].set_title(metric)

    # CALCULATE FAILURE RATE
    print(expon.pdf(linspace, scale=scale_) / (1 - expon.cdf(linspace, scale=scale_)))

    #plt.show()
    plt.show(block=False)


def plot_normal(name, metric, distribution, times, theoretical_distribution=None):
    mu = distribution[1]
    sigma = distribution[2]

    theoretical_mu = None
    theoretical_sigma = None
    # Checks whether there is a theoretical distribution to compare it to
    if theoretical_distribution is not None:
        theoretical_mu = theoretical_distribution[1]
        theoretical_sigma = theoretical_distribution[2]

    fig, subplots = setup_fig_subplots(metric)
    fig.suptitle(name)

    linspace = np.linspace(norm.ppf(0.001, loc=mu, scale=sigma), norm.ppf(0.999, loc=mu, scale=sigma), 1000)

    # First plot PDF
    if theoretical_distribution is not None:
        subplots[0].plot(linspace, norm.pdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[0].plot(linspace, norm.pdf(linspace, loc=theoretical_mu, scale=theoretical_sigma),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[0].legend()
    else:
        subplots[0].plot(linspace, norm.pdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6)

    if times != EMPTY_LIST:
        if metric == 'Reliability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to failures')
        if metric == 'Maintainability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to repairs')
        subplots[0].legend()
    subplots[0].set_title('Normal PDF')

    # Second plot CDF and/or Maintainability
    if theoretical_distribution is not None:
        subplots[1].plot(linspace, norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[1].plot(linspace, norm.cdf(linspace, loc=theoretical_mu, scale=theoretical_sigma),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[1].legend()
    else:
        subplots[1].plot(linspace, norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6)

    if metric == 'Reliability':
        subplots[1].set_title('Normal CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Normal CDF (Maintainability)')

    # Third plot Reliability
    if metric == 'Reliability':
        if theoretical_distribution is not None:
            subplots[2].plot(linspace, 1 - norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6,
                             label='Reconstructed')
            subplots[2].plot(linspace, 1 - norm.cdf(linspace, loc=theoretical_mu, scale=theoretical_sigma),
                             'b-', lw=1, alpha=0.6, label='Theoretical')
            subplots[2].legend()
        else:
            subplots[2].plot(linspace, 1 - norm.cdf(linspace, loc=mu, scale=sigma), 'r-', lw=1, alpha=0.6)
        subplots[2].set_title(metric)

    #plt.show()
    plt.show(block=False)


def plot_weibull(name, metric, distribution, times, theoretical_distribution=None):
    scale = distribution[1]
    shape = distribution[2]

    theoretical_scale = None
    theoretical_shape = None
    # Checks whether there is a theoretical distribution to compare it to
    if theoretical_distribution is not None:
        theoretical_scale = theoretical_distribution[1]
        theoretical_shape = theoretical_distribution[2]

    fig, subplots = setup_fig_subplots(metric)
    fig.suptitle(name)

    linspace = np.linspace(weibull_min.ppf(0.001, shape, loc=0, scale=scale),
                           weibull_min.ppf(0.999, shape, loc=0, scale=scale), 1000)

    # First plot PDF
    if theoretical_distribution is not None:
        subplots[0].plot(linspace, weibull_min.pdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[0].plot(linspace, weibull_min.pdf(linspace, theoretical_shape, loc=0, scale=theoretical_scale),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[0].legend()
    else:
        subplots[0].plot(linspace, weibull_min.pdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)

    if times != EMPTY_LIST:
        if metric == 'Reliability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to failures')
        if metric == 'Maintainability':
            subplots[0].hist(times, bins=20, normed=True, histtype='stepfilled', alpha=0.2, label='Time to repairs')
        subplots[0].legend()
    subplots[0].set_title('Weibull PDF')

    # Second plot CDF and/or Maintainability
    if theoretical_distribution is not None:
        subplots[1].plot(linspace, weibull_min.cdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[1].plot(linspace, weibull_min.cdf(linspace, theoretical_shape, loc=0, scale=theoretical_scale),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[1].legend()
    else:
        subplots[1].plot(linspace, weibull_min.cdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)

    if metric == 'Reliability':
        subplots[1].set_title('Weibull CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Weibull CDF (Maintainability)')

    # Third plot Reliability
    if metric == 'Reliability':
        if theoretical_distribution is not None:
            subplots[2].plot(linspace, 1 - weibull_min.cdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                             label='Reconstructed')
            subplots[2].plot(linspace, 1 - weibull_min.cdf(linspace, theoretical_shape, loc=0, scale=theoretical_scale),
                             'b-', lw=1, alpha=0.6, label='Theoretical')
            subplots[2].legend()
        else:
            subplots[2].plot(linspace, 1 - weibull_min.cdf(linspace, shape, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)
        subplots[2].set_title(metric)

    #plt.show()
    plt.show(block=False)


def plot_lognorm(name, metric, distribution, times, theoretical_distribution=None):
    # s = sigma and scale = exp(mu).
    mu = distribution[1]
    sigma = distribution[2]
    scale = math.exp(mu)

    theoretical_sigma = None
    theoretical_scale = None
    # Checks whether there is a theoretical distribution to compare it to
    if theoretical_distribution is not None:
        theoretical_mu = theoretical_distribution[1]
        theoretical_sigma = theoretical_distribution[2]
        theoretical_scale = math.exp(theoretical_mu)

    fig, subplots = setup_fig_subplots(metric)
    fig.suptitle(name)

    linspace = np.linspace(lognorm.ppf(0.001, sigma, loc=0, scale=scale),
                           lognorm.ppf(0.999, sigma, loc=0, scale=scale), 1000)

    # First plot PDF
    if theoretical_distribution is not None:
        subplots[0].plot(linspace, lognorm.pdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[0].plot(linspace, lognorm.pdf(linspace, theoretical_sigma, loc=0, scale=theoretical_scale),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[0].legend()
    else:
        subplots[0].plot(linspace, lognorm.pdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)

    if times != EMPTY_LIST:
        if metric == 'Reliability':
            subplots[0].hist(times, bins=50, normed=True, histtype='stepfilled', alpha=0.2, label='Time to failures')
        if metric == 'Maintainability':
            subplots[0].hist(times, bins=50, normed=True, histtype='stepfilled', alpha=0.2, label='Time to repairs')
        subplots[0].legend()
    subplots[0].set_title('Lognormal PDF')

    # Second plot CDF and/or Maintainability
    if theoretical_distribution is not None:
        subplots[1].plot(linspace, lognorm.cdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                         label='Reconstructed')
        subplots[1].plot(linspace, lognorm.cdf(linspace, theoretical_sigma, loc=0, scale=theoretical_scale),
                         'b-', lw=1, alpha=0.6, label='Theoretical')
        subplots[1].legend()
    else:
        subplots[1].plot(linspace, lognorm.cdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)

    if metric == 'Reliability':
        subplots[1].set_title('Lognormal CDF')
    if metric == 'Maintainability':
        subplots[1].set_title('Lognormal CDF (Maintainability)')

    # Third plot Reliability
    if metric == 'Reliability':
        if theoretical_distribution is not None:
            subplots[2].plot(linspace, 1 - lognorm.cdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6,
                             label='Reconstructed')
            subplots[2].plot(linspace, 1 - lognorm.cdf(linspace, theoretical_sigma, loc=0, scale=theoretical_scale),
                             'b-', lw=1, alpha=0.6, label='Theoretical')
            subplots[2].legend()
        else:
            subplots[2].plot(linspace, 1 - lognorm.cdf(linspace, sigma, loc=0, scale=scale), 'r-', lw=1, alpha=0.6)
        subplots[2].set_title(metric)

    #plt.show()
    plt.show(block=False)