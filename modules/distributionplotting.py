import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
import seaborn as sns


EMPTY_LIST = []


def differentiate(x, y):
    dy = np.zeros(y.shape, np.float)
    dy[0:-1] = np.diff(y) / np.diff(x)
    dy[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])

    return dy


def mean_squared_error(y, y_estimated):
    return np.square(y - y_estimated).mean()


def mse_exp(theoretical_distribution, estimated_distribution):
    theoretical_lambda= theoretical_distribution[1]
    theoretical_scale = 1/theoretical_lambda

    estimated_lambda = estimated_distribution[1]
    estimated_scale = 1 / estimated_lambda

    linspace = np.linspace(expon.ppf(0.001, scale=theoretical_scale), expon.ppf(0.999, scale=theoretical_scale), 1000)
    theoretical_pdf = expon.pdf(linspace, scale=theoretical_scale)
    estimated_pdf = expon.pdf(linspace, scale=estimated_scale)

    mse_pdf = mean_squared_error(theoretical_pdf, estimated_pdf)

    theoretical_cdf = expon.cdf(linspace, scale=theoretical_scale)
    estimated_cdf = expon.cdf(linspace, scale=estimated_scale)

    mse_cdf = mean_squared_error(theoretical_cdf, estimated_cdf)

    theoretical_reliability = 1 - expon.cdf(linspace, scale=theoretical_scale)
    estimated_reliability = 1 - expon.cdf(linspace, scale=estimated_scale)

    mse_reliability = mean_squared_error(theoretical_reliability, estimated_reliability)

    return [mse_pdf, mse_cdf, mse_reliability]


def setup_fig_subplots(metric):
    # Depending on Reliability or Maintainability the number of plots changes
    # Reliability has 3, Maintainability has only 2
    num_of_subplots = 0
    figure_width = 0

    if metric == 'Reliability':
        num_of_subplots = 3
        figure_width = 13
    if metric == 'Maintainability':
        num_of_subplots = 2
        figure_width = 9

    fig, subplots = plt.subplots(1, num_of_subplots, figsize=(figure_width, 4))
    return fig, subplots

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


def plot_arbitrary_distribution(name, times, linspace, theoretical_reliability=None):
    # Reliability for now
    # Maybe fix inconsistencies with the numbers on the axis
    fig, subplots = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle(name)

    # PDF
    sns.distplot(times, hist=True, ax=subplots[0])
    subplots[0].set_title('PDF')
    if theoretical_reliability is not None:
        theoretical_cdf = 1 - theoretical_reliability
        theoretical_pdf = differentiate(linspace, theoretical_cdf)
        subplots[0].plot(linspace, theoretical_pdf)

    # CDF
    sns.kdeplot(times, cumulative=True, ax=subplots[1])
    if theoretical_reliability is not None:
        theoretical_cdf = 1 - theoretical_reliability
        subplots[1].plot(linspace, theoretical_cdf)
    subplots[1].set_title('CDF')

    times.sort()
    samples = len(times)
    print('Samples: ' + str(samples))
    one_minus_cdf = [1 - (x / samples) for x in range(1, samples + 1)]
    # Get length of this and see if its the same length as the reliability of the top event
    # Better yet when calculating relability function use the same number of elements as the
    # length of top events time of failure or time of repair.
    # Reliability
    subplots[2].plot(times, one_minus_cdf)
    if theoretical_reliability is not None:
        subplots[2].plot(linspace, theoretical_reliability)
    subplots[2].set_ylim([0, 1.05])
    # For comparing graphs
    #subplots[2].set_xlim([0, 100])
    subplots[2].set_title('Reliability')

    # plt.show()
    plt.show(block=False)


def plot_():
    fig, subplot = plt.subplots(1, 1)
    #lambda_ = distribution[1]
    #scale_ = 1 / lambda_
    linspace = np.linspace(0, 10, 1000)

    rel = (1 - expon.cdf(linspace, expon.pdf(linspace, scale=5)))
    print(rel)

    subplot.plot(linspace, rel)

    plt.show()
