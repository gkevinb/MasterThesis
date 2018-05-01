from modules import timeseries
import scipy.stats
import pylab
from modules import distributionfitting as DF

size = 10000
x = scipy.arange(size)
y = timeseries._generate_numbers(['LOGNORM', 2, 1], size)
#y = timeseries._generate_numbers(['NORMAL', 15, 2], size)

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


d = DF.determine_distribution(y)
print(d)


# d = rel_weibull_dist = ['WEIBULL', 60, 10]
# d = ['LOGNORM', 5, 2]

print('MTTF (from data): ' + str(sum(y)/len(y)))
print('MTTF (from distribution): ' + str(DF.calculate_mttf_or_mttr_from_distribution(d)))
# scipy.stats.probplot(y, dist=scipy.stats.lognorm, sparams=(5, 2), plot=pylab)
# pylab.show()
print(scipy.stats.weibull_min.mean(10, 8))

# scipy.stats.probplot(y, dist=scipy.stats.norm, sparams=(2.5,), plot=pylab)
