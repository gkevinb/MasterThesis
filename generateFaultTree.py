from faultTreeContinuous import Event, Gate, FaultTree


# Find way to only allow events to connect with gates and vice versa,
# Event | Gate | Event | Gate | Event layers.

'''
topEvent = Event('Top Event')
or1 = Gate('OR', parent=topEvent)
basicEvent1 = Event('Basic Event 1', 'EXP', 10, 'EXP', 4, parent=or1)
basicEvent2 = Event('Basic Event 2', 'EXP', 10, 'EXP', 4, parent=or1)
intermed = Event('Inter event ', parent=or1)
and1 = Gate('AND', parent=intermed)
basicEvent3 = Event('Basic Event 3', 'EXP', 10, 'EXP', 4, parent=and1)
basicEvent4 = Event('Basic Event 4', 'EXP', 10, 'EXP', 4, parent=and1)
'''
'''
# k/N Voting Example
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
and2 = Gate('AND', parent=intermediateEvent1)
basicEvent1 = Event('Basic Event 1', 'EXP', 10, 'EXP', 4, parent=and2)
basicEvent2 = Event('Basic Event 2', 'EXP', 10, 'EXP', 4, parent=and2)
vote = Gate('VOTING', parent=intermediateEvent2, k=2)
basicEvent3 = Event('Basic Event 3', 'EXP', 10, 'EXP', 4, parent=vote)
basicEvent4 = Event('Basic Event 4', 'EXP', 10, 'EXP', 4, parent=vote)
basicEvent5 = Event('Basic Event 5', 'EXP', 10, 'EXP', 4, parent=vote)
'''

'''
# RECONSTRUCTED FAULT TREE
top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
basic_event_3 = Event("Basic Event 3", parent=voting2)
basic_event_4 = Event("Basic Event 4", parent=voting2)
basic_event_5 = Event("Basic Event 5", parent=voting2)
and3 = Gate("AND", parent=intermediate_event_2)
basic_event_1 = Event("Basic Event 1", parent=and3)
basic_event_2 = Event("Basic Event 2", parent=and3)
'''

rel_exp_dist = ['EXP', 10]
main_exp_dist = ['EXP', 4]
rel_weibull_dist = ['WEIBULL', 10, 8]
main_weibull_dist = ['WEIBULL', 4, 10]


topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=vote2)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=vote2)
intermediateEvent3 = Event('Intermediate Event 3', parent=vote2)
and2 = Gate('AND', parent=intermediateEvent3)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=and2)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist,  parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent5 = Event('Basic Event 5', rel_exp_dist, main_exp_dist, parent=or1)
intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
and3 = Gate('AND', parent=intermediateEvent4)
basicEvent6 = Event('Basic Event 6', rel_exp_dist, main_exp_dist, parent=and3)
basicEvent7 = Event('Basic Event 7', rel_exp_dist, main_exp_dist,  parent=and3)
basicEvent8 = Event('Basic Event 8', rel_exp_dist, main_exp_dist,  parent=and3)

'''
# RECONSTRUCTED FAULT TREE
top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
or2 = Gate("OR", parent=intermediate_event_1)
intermediate_event_3 = Event("Intermediate Event 3", parent=or2)
basic_event_5 = Event("Basic Event 5", parent=or2)
voting3 = Gate("VOTING", parent=intermediate_event_2, k=2)
intermediate_event_4 = Event("Intermediate Event 4", parent=voting3)
basic_event_1 = Event("Basic Event 1", parent=voting3)
basic_event_2 = Event("Basic Event 2", parent=voting3)
and4 = Gate("AND", parent=intermediate_event_3)
basic_event_6 = Event("Basic Event 6", parent=and4)
basic_event_7 = Event("Basic Event 7", parent=and4)
basic_event_8 = Event("Basic Event 8", parent=and4)
and5 = Gate("AND", parent=intermediate_event_4)
basic_event_3 = Event("Basic Event 3", parent=and5)
basic_event_4 = Event("Basic Event 4", parent=and5)
'''

fault_tree = FaultTree(topEvent)
# 10000 generation size takes a good minute
# 100000 takes more than 10 minutes didn't wait to finish
fault_tree.generate_basic_event_time_series(1000)
fault_tree.calculate_time_series()
fault_tree.print_tree()
fault_tree.export_time_series('time_series.txt')
