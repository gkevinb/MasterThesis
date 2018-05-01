from faultTreeContinuous import Event, Gate, FaultTree
import matplotlib.pyplot as plt
import math
from scipy.stats import expon, norm, weibull_min, lognorm
import numpy as np


rel_exp_dist = ['EXP', 1/40]
lognorm = ['LOGNORM', 2, 1]
norm = ['NORMAL', 15, 2]
main_exp_dist = ['EXP', 1/10]
rel_weibull_dist = ['WEIBULL', 10, 8]
main_weibull_dist = ['WEIBULL', 4, 10]

'''
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
and2 = Gate('AND', parent=intermediateEvent1)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=and2)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=or1)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist, parent=or1)
'''

topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=vote2)
basicEvent2 = Event('Basic Event 2', rel_weibull_dist, main_exp_dist, parent=vote2)
intermediateEvent3 = Event('Intermediate Event 3', parent=vote2)
and2 = Gate('AND', parent=intermediateEvent3)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, rel_weibull_dist, parent=and2)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist,  parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent5 = Event('Basic Event 5', norm, main_exp_dist, parent=or1)
intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
and3 = Gate('AND', parent=intermediateEvent4)
basicEvent6 = Event('Basic Event 6', rel_exp_dist, lognorm, parent=and3)
basicEvent7 = Event('Basic Event 7', lognorm, main_exp_dist,  parent=and3)
basicEvent8 = Event('Basic Event 8', rel_exp_dist, norm,  parent=and3)

FT = FaultTree(topEvent)
FT.print_tree()

# FT.plot_reliability_distribution_of_basic_event_(1)
FT.plot_reliability_distribution_of_basic_event_(2)

linspace = np.linspace(0, 100, 1000)
FT.calculate_reliability(linspace)


print(FT.top_event.reliability_function)


fig, subplot = plt.subplots(1, 1)
subplot.plot(linspace, FT.top_event.reliability_function)
plt.show()
