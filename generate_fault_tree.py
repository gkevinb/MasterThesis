from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree

rel_exp_dist = ['EXP', 1 / 3]
main_exp_dist = ['EXP', 1 / 2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 4, 1]
weibull = ['WEIBULL', 5, 2]
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

FT = FaultTree(top_event)

FT.generate_basic_event_time_series(4)

FT.calculate_time_series()

FT.print_tree()

FT.export_time_series('times.txt')
