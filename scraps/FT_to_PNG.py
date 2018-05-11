from faultTreeContinuous import Event, Gate, FaultTree
from anytree.exporter import DotExporter
from modules import FTVisualizer
import matplotlib.pyplot as plt


rel_exp_dist = ['EXP', 1/3]
main_exp_dist = ['EXP', 1/2]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 4, 1]

'''
topEvent = Event('Top Event')
or1 = Gate('AND', parent=topEvent)
basicEvent1 = Event('Basic Event 1', norm_dist, main_exp_dist, parent=or1)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=or1)
'''

topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=vote2)
basicEvent2 = Event('Basic Event 2', main_exp_dist, main_exp_dist, parent=vote2)
intermediateEvent3 = Event('Intermediate Event 3', parent=vote2)
and2 = Gate('AND', parent=intermediateEvent3)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=and2)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist,  parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent5 = Event('Basic Event 5', norm_dist, main_exp_dist, parent=or1)
intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
and3 = Gate('AND', parent=intermediateEvent4)
basicEvent6 = Event('Basic Event 6', rel_exp_dist, main_exp_dist, parent=and3)
basicEvent7 = Event('Basic Event 7', norm_dist, main_exp_dist,  parent=and3)
basicEvent8 = Event('Basic Event 8', rel_exp_dist, main_exp_dist,  parent=and3)


FT = FaultTree(topEvent)
FT.print_tree()

FTVisualizer.export_to_png(FT, 'ft3.png')
