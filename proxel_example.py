from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree
import matplotlib.pyplot as plt


rel_exp_dist = ['EXP', 1/3]
main_exp_dist = ['EXP', 1/2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 4, 1]
weibull = ['WEIBULL', 3, 2]

'''
top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
basic_event_3 = Event("Basic Event 3", norm_dist, main_exp_dist, parent=voting2)
basic_event_4 = Event("Basic Event 4", rel_exp_dist, weibull, parent=voting2)
basic_event_5 = Event("Basic Event 5", lognorm_dist, main_exp_dist, parent=voting2)
or3 = Gate("OR", parent=intermediate_event_2)
basic_event_1 = Event("Basic Event 1", norm_dist, main_exp_dist, parent=or3)
basic_event_2 = Event("Basic Event 2", rel_exp_dist, norm_dist, parent=or3)
'''
'''
top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
and2 = Gate("AND", parent=intermediate_event_1, k=2)
basic_event_1 = Event("Basic Event 1", norm_dist, main_exp_dist, parent=and2)
basic_event_2 = Event("Basic Event 2", rel_exp_dist, norm_dist, parent=and2)
or3 = Gate("OR", parent=intermediate_event_2)
basic_event_3 = Event("Basic Event 3", norm_dist, main_exp_dist, parent=or3)
basic_event_4 = Event("Basic Event 4",  lognorm_dist, weibull, parent=or3)
'''

top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
and2 = Gate("AND", parent=intermediate_event_1, k=2)
basic_event_1 = Event("Basic Event 1", ["NORMAL", 3.9830144614706033, 0.9862341075243011], ["EXP", 0.48906000112507997], parent=and2)
basic_event_2 = Event("Basic Event 2", ["EXP", 0.3413575302109938], ["NORMAL", 4.027387262161776, 1.0093318673285416], parent=and2)
or3 = Gate("OR", parent=intermediate_event_2)
basic_event_3 = Event("Basic Event 3", ["NORMAL", 3.9992910990394113, 1.0001655493233952], ["EXP", 0.5064322512357143], parent=or3)
basic_event_4 = Event("Basic Event 4",  ["LOGNORM", 1.980572752250706, 0.9902566667103683], ["WEIBULL", 5.014524329049925, 1.9732736816578598], parent=or3)


FT = FaultTree(top_event)
FT.print_tree()

#linspace = np.linspace(0, 100, 1000)

#FT.calculate_reliability_maintainability(linspace)
#y = basicEvent1.reliability_function
#y_ = basicEvent1.maintainability_function

FT.calculate_proxel_probalities(0.5, 12)
FT.plot_probability_of_ok_of_basic_event_(1)
FT.plot_probability_of_ok_of_basic_event_(2)
FT.plot_probability_of_ok_of_basic_event_(3)
FT.plot_probability_of_ok_of_basic_event_(4)
FT.plot_probability_of_ok_of_top_event()
plt.show()
