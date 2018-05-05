from faultTreeContinuous import Event, Gate, FaultTree
import matplotlib.pyplot as plt
import numpy as np


rel_exp_dist = ['EXP', 1/10]
main_exp_dist = ['EXP', 1/5]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 240, 10]


topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=and1)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=and1)

FT = FaultTree(topEvent)
FT.print_tree()

linspace = np.linspace(0, 100, 1000)

FT.calculate_reliability_maintainability(linspace)
y = basicEvent1.reliability_function
y_ = basicEvent1.maintainability_function

plt.plot(linspace, y, linspace, y_)
plt.show()
