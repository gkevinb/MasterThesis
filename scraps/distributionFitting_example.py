from modules import timeseries
import scipy.stats
import numpy
import math
from modules import distributionfitting as DF

size = 1500
x = scipy.arange(size)
#y = timeseries._generate_numbers(['LOGNORM', 2, 1], size)
#y = timeseries._generate_numbers(['NORMAL', 15, 2], size)

#y = timeseries._generate_numbers(['EXP', 1/5], size)
#y = timeseries._generate_numbers(['WEIBULL', 60, 10], size)
#y = timeseries._generate_numbers(['WEIBULL', 10, 8], size)


def CI(array):
    X = numpy.mean(array)
    s = numpy.std(array)
    n = len(array)
    z = 1.96

    ci_min = X - z * (s / math.sqrt(n))
    ci_max = X + z * (s / math.sqrt(n))

    return [ci_min, ci_max]


sizes = [100, 500, 1000, 5000, 10000]

for i in range(0, len(sizes)):
    print(sizes[i])
    unidentified = 0
    a = []
    b = []
    for j in range(0, 10):
        y = timeseries._generate_numbers(['WEIBULL', 10, 8], sizes[i])
        d = DF.determine_distribution(y)
        print(d)
        if d[0] == 'UNIDENTIFIED DISTRIBUTION':
            unidentified += 1
        else:
            a.append(d[1])
            b.append(d[2])
    print('Identified: ' + str(10 - unidentified) + ' out of 10')
    print('CI: ' + str(CI(a)))
    print('CI: ' + str(CI(b)))




#d = DF.determine_distribution(y)
#print(d)


# d = rel_weibull_dist = ['WEIBULL', 60, 10]
# d = ['LOGNORM', 5, 2]

print('MTTF (from data): ' + str(sum(y)/len(y)))
print('MTTF (from distribution): ' + str(DF.calculate_mttf_or_mttr_from_distribution(d)))
# scipy.stats.probplot(y, dist=scipy.stats.lognorm, sparams=(5, 2), plot=pylab)
# pylab.show()
#print(scipy.stats.weibull_min.mean(10, 8))

# scipy.stats.probplot(y, dist=scipy.stats.norm, sparams=(2.5,), plot=pylab)
