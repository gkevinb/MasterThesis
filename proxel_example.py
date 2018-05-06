from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree
import matplotlib.pyplot as plt


rel_exp_dist = ['EXP', 1/3]
main_exp_dist = ['EXP', 1/2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 4, 1]


topEvent = Event('Top Event')
or1 = Gate('AND', parent=topEvent)
basicEvent1 = Event('Basic Event 1', norm_dist, main_exp_dist, parent=or1)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=or1)


FT = FaultTree(topEvent)
FT.print_tree()

#linspace = np.linspace(0, 100, 1000)

#FT.calculate_reliability_maintainability(linspace)
#y = basicEvent1.reliability_function
#y_ = basicEvent1.maintainability_function

FT.calculate_proxel_probalities(0.5, 6)
#FT.plot_probability_of_failure_of_basic_event_(1)
#FT.plot_probability_of_failure_of_basic_event_(2)
FT.plot_probability_of_failure_of_top_event()
plt.show()
