from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree

rel_exp_dist = ['EXP', 1 / 3]
main_exp_dist = ['EXP', 1 / 2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 5, 1]
weibull_dist = ['WEIBULL', 10, 8]


def A():

    top_event = Event("Top Event")
    and1 = Gate("AND", parent=top_event)
    intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
    intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
    voting2 = Gate("VOTING", parent=intermediate_event_1, k=3)
    basic_event_4 = Event("Basic Event 4", rel_exp_dist, lognorm_dist, parent=voting2)
    basic_event_5 = Event("Basic Event 5", norm_dist, main_exp_dist, parent=voting2)
    basic_event_6 = Event("Basic Event 6", lognorm_dist, main_exp_dist, parent=voting2)
    voting3 = Gate("VOTING", parent=intermediate_event_2, k=1)
    basic_event_1 = Event("Basic Event 1", weibull_dist, main_exp_dist, parent=voting3)
    basic_event_2 = Event("Basic Event 2", rel_exp_dist, lognorm_dist, parent=voting3)
    basic_event_3 = Event("Basic Event 3", weibull_dist, main_exp_dist, parent=voting3)

    fault_tree = FaultTree(top_event)

    return fault_tree


def B():
    topEvent = Event('Top Event')
    and1 = Gate('AND', parent=topEvent)
    basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=and1)
    basicEvent2 = Event('Basic Event 2', ['EXP', 1 / 6], main_exp_dist, parent=and1)

    fault_tree = FaultTree(topEvent)

    return fault_tree


def C():
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
    basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist, parent=and2)
    or1 = Gate('OR', parent=intermediateEvent2)
    basicEvent5 = Event('Basic Event 5', rel_exp_dist, main_exp_dist, parent=or1)
    intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
    and3 = Gate('AND', parent=intermediateEvent4)
    basicEvent6 = Event('Basic Event 6', rel_exp_dist, main_exp_dist, parent=and3)
    basicEvent7 = Event('Basic Event 7', rel_exp_dist, main_exp_dist, parent=and3)
    basicEvent8 = Event('Basic Event 8', rel_exp_dist, main_exp_dist, parent=and3)

    fault_tree = FaultTree(topEvent)

    return fault_tree


def D():
    topEvent = Event('Top Event')
    or1 = Gate('OR', parent=topEvent)
    intermediateEvent1 = Event('Intermediate Event 1', parent=or1)
    intermediateEvent2 = Event('Intermediate Event 2', parent=or1)
    vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
    basicEvent1 = Event('Basic Event 1', lognorm_dist, norm_dist, parent=vote2)
    basicEvent2 = Event('Basic Event 2', rel_exp_dist, weibull_dist, parent=vote2)
    basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=vote2)
    and2 = Gate('AND', parent=intermediateEvent2)
    basicEvent4 = Event('Basic Event 4', norm_dist, main_exp_dist, parent=and2)
    basicEvent5 = Event('Basic Event 5', ['EXP', 1 / 10], lognorm_dist, parent=and2)

    fault_tree = FaultTree(topEvent)

    return fault_tree
