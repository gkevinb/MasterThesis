import matplotlib.pyplot as plt
import scipy
from modules import timeseries
import scipy.stats
size = 50000
x = scipy.arange(size)
y = timeseries._generate_numbers(['LOGNORMAL', 5, 2], size)
#y = timeseries._generate_numbers(['EXP', 1/5], 10000)
#y = timeseries._generate_numbers(['WEIBULL', 60, 10], 50000)
# creating the dummy sample (using beta distribution)
# creating the histogram
h = plt.hist(y, bins=range(48))

dist_names = ['lognorm', 'weibull_min', 'weibull_max', 'expon']

for dist_name in dist_names:
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(y)
    print('Parameters for ' + str(dist_name) + ' : ' + str(param))
    print(scipy.stats.kstest(y, dist_name, scipy.stats.lognorm.fit(y)))
    pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
    plt.plot(pdf_fitted, label=dist_name)
    plt.xlim(0,47)
plt.legend(loc='upper left')
plt.show()