import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np
from modules import distributionfitting

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

exp = ['EXP', 0.5]
normal = ['NORMAL', 5, 1]
ln = ['LOGNORM', 0, 1]
wb = ['WEIBULL', 1, 1.5]

print(distributionfitting.calculate_mttf_or_mttr_from_distribution(ln))

lin_space = np.linspace(0, 20, 1000)
# a = np.empty(100)
# a.fill(0.5)
theoretical_pdf_05 = calculate_pdf(['LOGNORM', 0, 1], lin_space)
theoretical_pdf_1 = calculate_pdf(['LOGNORM', 1, 1], lin_space)
theoretical_pdf_15 = calculate_pdf(['WEIBULL', 10, 8], lin_space)
theoretical_pdf_5 = calculate_pdf(['WEIBULL', 1, 5], lin_space)
theoretical_cdf_05 = calculate_cdf(['WEIBULL', 1, 0.5], lin_space)
theoretical_cdf_1 = calculate_cdf(['WEIBULL', 1, 1], lin_space)
theoretical_cdf_15 = calculate_cdf(['WEIBULL', 1, 1.5], lin_space)
theoretical_cdf_5 = calculate_cdf(['WEIBULL', 1, 5], lin_space)
subplots.plot(lin_space, theoretical_pdf_15, 'r-', lw=1.5, alpha=0.6, label="\u03B2 = 0.5")
#subplots.plot(lin_space, theoretical_pdf_05, 'g-', lw=1.5, alpha=0.6, label="\u03B2 = 1.0")
#subplots.plot(lin_space, theoretical_cdf_15, 'b-', lw=1.5, alpha=0.6, label="\u03B2 = 1.5")
#subplots.plot(lin_space, theoretical_cdf_5, 'c-', lw=1.5, alpha=0.6, label="\u03B2 = 1.5")
subplots.set_xlabel('t')
#subplots.set_ylabel('P(t)')
subplots.set_ylabel('P(T\u2264t)')
#subplots.set_ylim([0, 1.1])
subplots.legend()
#subplots.set_ylabel('\u03BB(t)')

plt.show()

