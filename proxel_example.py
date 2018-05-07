from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree
import matplotlib.pyplot as plt


rel_exp_dist = ['EXP', 1/3]
main_exp_dist = ['EXP', 1/2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 4, 1]

top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
basic_event_3 = Event("Basic Event 3", rel_exp_dist, main_exp_dist, parent=voting2)
basic_event_4 = Event("Basic Event 4", norm_dist, main_exp_dist, parent=voting2)
basic_event_5 = Event("Basic Event 5", rel_exp_dist, main_exp_dist, parent=voting2)
or3 = Gate("OR", parent=intermediate_event_2)
basic_event_1 = Event("Basic Event 1", norm_dist, main_exp_dist, parent=or3)
basic_event_2 = Event("Basic Event 2", rel_exp_dist, main_exp_dist, parent=or3)

FT = FaultTree(top_event)
FT.print_tree()

#linspace = np.linspace(0, 100, 1000)

#FT.calculate_reliability_maintainability(linspace)
#y = basicEvent1.reliability_function
#y_ = basicEvent1.maintainability_function

FT.calculate_proxel_probalities(0.5, 8)
#FT.plot_probability_of_failure_of_basic_event_(1)
#FT.plot_probability_of_failure_of_basic_event_(2)
FT.plot_probability_of_failure_of_top_event()
plt.show()
